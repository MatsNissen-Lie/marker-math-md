#!/usr/bin/env python3
"""One-off helper to convert PDFs in the inbox or from argv using the package logic."""

import logging
import sys
from pathlib import Path
from typing import Iterable

from pdf_converter.conversion import (
    convert_pdf,
    ensure_outdir,
    gather_inbox_pdfs,
    resolve_pdf_paths,
)


def _filter_unconverted(pdfs: Iterable[Path], outdir: Path) -> list[Path]:
    filtered: list[Path] = []
    for pdf in pdfs:
        out_md = outdir / f"{pdf.stem}.md"
        if out_md.exists():
            logging.info("[skip] %s already converted", pdf.name)
            continue
        filtered.append(pdf)
    return filtered


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger("pdf2md_best_plus")

    base_dir = Path(__file__).resolve().parent
    outdir = ensure_outdir(base_dir)

    argv_pdfs = resolve_pdf_paths(sys.argv[1:])
    if argv_pdfs:
        pdfs = _filter_unconverted(argv_pdfs, outdir)
        if not pdfs:
            logger.info("No PDFs require conversion. Exiting.")
            return 0
    else:
        pdfs = gather_inbox_pdfs(base_dir / "inbox", outdir)
        if not pdfs:
            logger.info("No unprocessed PDFs found in ./inbox. Exiting.")
            return 0

    converted = 0
    for pdf in pdfs:
        try:
            logger.info("[convert] %s", pdf.name)
            convert_pdf(pdf, outdir, logger=logger)
            converted += 1
        except RuntimeError as exc:
            logger.error("%s", exc)
            return 1
        except Exception as exc:  # pragma: no cover - defensive
            logger.error("[fail] %s: %s", pdf.name, exc)

    logger.info("\nDone. Converted %d file(s) to: %s", converted, outdir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
