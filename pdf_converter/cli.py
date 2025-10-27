"""Command-line entry point for the inbox watcher."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from .watcher import run_inbox_watcher

DEFAULT_RUNTIME = 60 * 60  # 1 hour
DEFAULT_POLL_INTERVAL = 1.0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Watch an inbox folder and convert PDFs to Markdown using Marker.")
    parser.add_argument(
        "--runtime-seconds",
        type=int,
        default=DEFAULT_RUNTIME,
        help="How long to run the watcher before exiting (0 disables the limit).",
    )
    parser.add_argument(
        "--inbox",
        type=Path,
        default=Path("inbox"),
        help="Relative path to the inbox directory to watch.",
    )
    parser.add_argument(
        "--outdir",
        type=Path,
        default=Path("markdown"),
        help="Relative path for Markdown output.",
    )
    parser.add_argument(
        "--poll-interval",
        type=float,
        default=DEFAULT_POLL_INTERVAL,
        help="Watcher main-loop sleep interval in seconds.",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip the optional OpenAI cleanup even if OPENAI_API_KEY is set.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity level.",
    )
    return parser


def configure_logging(level: str) -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    return logging.getLogger("pdf_converter")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    logger = configure_logging(args.log_level)

    base_dir = Path.cwd()
    inbox_dir = (base_dir / args.inbox).resolve()
    outdir = (base_dir / args.outdir).resolve()

    logger.info("Starting PDF inbox watcher")
    logger.info("Inbox: %s", inbox_dir)
    logger.info("Output: %s", outdir)

    run_inbox_watcher(
        inbox_dir=inbox_dir,
        outdir=outdir,
        runtime_seconds=args.runtime_seconds,
        apply_llm=not args.no_llm,
        poll_interval=args.poll_interval,
        logger=logger,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
