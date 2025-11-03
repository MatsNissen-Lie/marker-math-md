"""Filesystem watcher that converts PDFs dropped into an inbox directory."""

from __future__ import annotations

import logging
import os
import queue
import threading
import time
from pathlib import Path
from typing import Iterable, Union, cast

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .conversion import MarkerOptions, convert_pdf, gather_inbox_pdfs, is_pdf

LOGGER = logging.getLogger(__name__)

OSPathish = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]
ExtendedPathish = Union[OSPathish, bytearray, memoryview]


def _to_path(value: ExtendedPathish | Path) -> Path:
    if isinstance(value, Path):
        return value
    os_compatible: OSPathish
    if isinstance(value, (bytearray, memoryview)):
        os_compatible = bytes(value)
    else:
        os_compatible = cast(OSPathish, value)
    return Path(os.fsdecode(os_compatible))


class ConversionWorker:
    """Background worker that serializes PDF conversions."""

    def __init__(
        self,
        outdir: Path,
        *,
        marker_options: MarkerOptions,
        logger: logging.Logger | None = None,
        max_files: int | None = None,
    ):
        self._outdir = outdir
        self._marker_options = marker_options
        self._logger = logger or LOGGER
        self._queue: "queue.Queue[Path | None]" = queue.Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._run, name="pdf-convert-worker", daemon=True
        )
        self._pending: set[Path] = set()
        normalized_limit = max_files if max_files and max_files > 0 else None
        self._max_files: int | None = normalized_limit
        self._processed = 0
        self._limit_reached = threading.Event()

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._queue.put(None)
        self._thread.join()

    def submit(self, pdf_path: Path) -> bool:
        pdf_path = pdf_path.resolve()
        if self._stop.is_set() or self._limit_reached.is_set():
            return False
        if self._max_files is not None and (
            self._processed + len(self._pending)
        ) >= self._max_files:
            self._limit_reached.set()
            return False
        if pdf_path in self._pending:
            return False
        if not is_pdf(pdf_path):
            return False
        self._pending.add(pdf_path)
        self._queue.put(pdf_path)
        return True

    def preload(self, pdfs: Iterable[Path]) -> int:
        queued = 0
        for pdf in pdfs:
            if self.submit(pdf):
                queued += 1
            elif self._limit_reached.is_set():
                break
        return queued

    @property
    def processed(self) -> int:
        return self._processed

    @property
    def max_files(self) -> int | None:
        return self._max_files

    @property
    def limit_reached(self) -> bool:
        return self._limit_reached.is_set()

    def _run(self) -> None:
        while True:
            try:
                item = self._queue.get(timeout=0.5)
            except queue.Empty:
                if self._stop.is_set():
                    break
                continue

            if item is None:
                break

            pdf_path = item
            try:
                if not self._wait_until_ready(pdf_path):
                    self._logger.warning("[skip] %s never became ready", pdf_path.name)
                    continue
                converted = convert_pdf(
                    pdf_path,
                    self._outdir,
                    options=self._marker_options,
                    logger=self._logger,
                )
                if converted:
                    self._processed += 1
                    if self._max_files is not None and self._processed >= self._max_files:
                        self._limit_reached.set()
                        self._logger.info(
                            "[limit] Reached maximum of %s converted PDFs", self._max_files
                        )
                        self._stop.set()
            except Exception as exc:
                self._logger.error("[fail] %s: %s", pdf_path.name, exc)
            finally:
                self._pending.discard(pdf_path)
                self._queue.task_done()

    def _wait_until_ready(
        self, pdf_path: Path, *, attempts: int = 10, delay: float = 1.0
    ) -> bool:
        last_size = -1
        for _ in range(attempts):
            if not pdf_path.exists():
                time.sleep(delay)
                continue
            try:
                size = pdf_path.stat().st_size
            except OSError:
                time.sleep(delay)
                continue
            if size == last_size and size > 0:
                return True
            last_size = size
            time.sleep(delay)
        return pdf_path.exists()


class InboxEventHandler(FileSystemEventHandler):
    def __init__(self, worker: ConversionWorker, logger: logging.Logger | None = None):
        self._worker = worker
        self._logger = logger or LOGGER

    def on_created(self, event):  # type: ignore[override]
        if event.is_directory:
            return
        self._handle_path(_to_path(event.src_path))

    def on_moved(self, event):  # type: ignore[override]
        if event.is_directory:
            return
        self._handle_path(_to_path(event.dest_path))

    def _handle_path(self, path: Path) -> None:
        if not is_pdf(path):
            return
        if self._worker.submit(path):
            self._logger.info("[queue] %s", path.name)
        elif self._worker.limit_reached:
            self._logger.info("[skip] %s (max files reached)", path.name)


def run_inbox_watcher(
    inbox_dir: Path,
    outdir: Path,
    *,
    runtime_seconds: int,
    marker_options: MarkerOptions,
    poll_interval: float,
    max_files: int = 0,
    logger: logging.Logger | None = None,
) -> None:
    inbox_dir.mkdir(parents=True, exist_ok=True)
    outdir.mkdir(parents=True, exist_ok=True)

    logger = logger or LOGGER
    worker = ConversionWorker(
        outdir,
        marker_options=marker_options,
        logger=logger,
        max_files=max_files,
    )
    handler = InboxEventHandler(worker, logger=logger)
    observer = Observer()
    observer.schedule(handler, str(inbox_dir), recursive=False)

    logger.info(
        "Watching %s for new PDFs (runtime limit: %s seconds)",
        inbox_dir,
        runtime_seconds,
    )

    worker.start()
    backlog = gather_inbox_pdfs(inbox_dir, outdir)
    if backlog:
        queued = worker.preload(backlog)
        if queued:
            logger.info("Found %d existing PDFs to convert", queued)
        elif worker.limit_reached:
            logger.info(
                "Max files limit reached before processing existing backlog; %d PDFs left",
                len(backlog),
            )

    observer.start()
    deadline = time.monotonic() + runtime_seconds if runtime_seconds > 0 else None
    limit_logged = False

    try:
        while True:
            if worker.limit_reached:
                if not limit_logged:
                    cap = worker.max_files or max_files
                    logger.info(
                        "Max files limit (%s) reached; shutting down watcher.",
                        cap,
                    )
                    limit_logged = True
                break
            if deadline is not None and time.monotonic() >= deadline:
                logger.info("Runtime limit reached; shutting down watcher.")
                break
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        logger.info("Received interrupt; stopping watcher.")
    finally:
        observer.stop()
        observer.join()
        worker.stop()
        logger.info("Watcher stopped.")


__all__ = ["run_inbox_watcher"]
