"""Command-line entry point for the inbox watcher."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from dotenv import load_dotenv
from .conversion import DEFAULT_LLM_SERVICE, MarkerOptions
from .watcher import run_inbox_watcher

DEFAULT_RUNTIME = 60 * 60  # 1 hour
DEFAULT_POLL_INTERVAL = 1.0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Watch an inbox folder and convert PDFs to Markdown using Marker."
    )
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
        "--use-llm",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable Marker hybrid mode; pass --no-use-llm to disable.",
    )
    parser.add_argument(
        "--force-ocr",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Force OCR on all lines (--no-force-ocr to disable).",
    )
    parser.add_argument(
        "--strip-existing-ocr",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Strip embedded OCR text before processing (helps noisy PDFs).",
    )
    parser.add_argument(
        "--redo-inline-math",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Re-run inline math detection for highest fidelity (--no-redo-inline-math to disable).",
    )
    parser.add_argument(
        "--llm-service",
        default=DEFAULT_LLM_SERVICE,
        help="Fully-qualified Marker LLM service class, e.g. marker.services.gemini.GoogleGeminiService.",
    )
    parser.add_argument(
        "--gemini-api-key",
        default=None,
        help="API key for Google Gemini when using the Gemini service.",
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

    load_dotenv(dotenv_path=base_dir / ".env", override=False)

    logger.info("Starting PDF inbox watcher")
    logger.info("Inbox: %s", inbox_dir)
    logger.info("Output: %s", outdir)

    marker_options = MarkerOptions(
        use_llm=args.use_llm,
        force_ocr=args.force_ocr,
        strip_existing_ocr=args.strip_existing_ocr,
        redo_inline_math=args.redo_inline_math,
        llm_service=args.llm_service,
        gemini_api_key=args.gemini_api_key,
    )
    logger.info("Marker options: %s", marker_options.describe())

    run_inbox_watcher(
        inbox_dir=inbox_dir,
        outdir=outdir,
        runtime_seconds=args.runtime_seconds,
        marker_options=marker_options,
        poll_interval=args.poll_interval,
        logger=logger,
    )

    logger.info("Watcher finished with options: %s", marker_options.describe())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
