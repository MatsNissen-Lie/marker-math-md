#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zero-arg PDF -> Markdown watcher (Marker only).

- Uses Marker as a library (no external LLMs or post-processors).
- Creates ./inbox and ./markdown next to this script.
- Converts each new *.pdf in ./inbox to ./markdown/<name>.md.
- Skips non-PDF files and already-converted basenames.
- Watches continuously until Ctrl+C.

Install:
    pip install marker-pdf

Optional (Marker-built-in features via env):
    # Use Marker hybrid mode (requires Marker-supported LLM service keys)
    export MARKER_USE_LLM=1
    # Force OCR for all lines (helps inline math when PDFs have bad text)
    export MARKER_FORCE_OCR=1
    # Strip existing OCR text (if PDF has messy OCR you want removed)
    export MARKER_STRIP_EXISTING_OCR=1
    # Redo inline math (pairs well with use_llm)
    export MARKER_REDO_INLINE_MATH=1
    # Select LLM service explicitly (defaults to Gemini if configured)
    # e.g.: marker.services.openai.OpenAIService, marker.services.gemini.GoogleGeminiService, etc.
    export MARKER_LLM_SERVICE="marker.services.gemini.GoogleGeminiService"
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Set, Optional

# ---- settings (tweak if you want) ----
IN_DIR_NAME = "inbox"
OUT_DIR_NAME = "markdown"
POLL_INTERVAL_SEC = 3.0
# --------------------------------------

LOG = logging.getLogger("pdf2md_marker_watch")
logging.basicConfig(level=logging.INFO, format="%(message)s")

INSTALL_HINT = "pip install marker-pdf"

def script_dir() -> Path:
    return Path(__file__).resolve().parent

def in_dir() -> Path:
    p = script_dir() / IN_DIR_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p

def out_dir() -> Path:
    p = script_dir() / OUT_DIR_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p

def is_pdf(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() == ".pdf" and not p.name.startswith(".")

def md_for(pdf_path: Path) -> Path:
    return out_dir() / f"{pdf_path.stem}.md"

# ----- Marker wiring (library, not CLI) -----
# We stick to Marker only. No external LLMs or post-processors here.
# If you set env like MARKER_USE_LLM=1, Marker itself will use the configured backend.

_converter = None

def _build_marker_converter():
    """
    Build a Marker PdfConverter with optional config derived from environment.
    """
    try:
        from marker.converters.pdf import PdfConverter  # type: ignore
        from marker.models import create_model_dict     # type: ignore
        # Optional config path using Marker ConfigParser (only if we need to set flags)
        from marker.config.parser import ConfigParser   # type: ignore
    except Exception as exc:
        raise RuntimeError(
            f"Marker is not installed. Install it with: {INSTALL_HINT}"
        ) from exc

    cfg: dict = {}
    # output_format defaults to markdown; keep it explicit anyway
    cfg["output_format"] = "markdown"

    # Read env toggles to stay “no-args” while letting you flip Marker features
    if os.getenv("MARKER_USE_LLM"):
        cfg["use_llm"] = True
    if os.getenv("MARKER_FORCE_OCR"):
        cfg["force_ocr"] = True
    if os.getenv("MARKER_STRIP_EXISTING_OCR"):
        cfg["strip_existing_ocr"] = True
    if os.getenv("MARKER_REDO_INLINE_MATH"):
        cfg["redo_inline_math"] = True

    # Choose an LLM service class if provided (Marker-only feature; optional)
    llm_service = None
    llm_service_path = os.getenv("MARKER_LLM_SERVICE")
    if llm_service_path:
        # The ConfigParser can wire this; if not provided, Marker uses its default
        pass

    models = create_model_dict()
    if cfg:
        # If we have any config, wire via ConfigParser so Marker honors it
        ConfigParser = __import__("marker.config.parser", fromlist=["ConfigParser"]).config.parser.ConfigParser  # type: ignore  # noqa
        cp = ConfigParser(cfg)
        return PdfConverter(
            config=cp.generate_config_dict(),
            artifact_dict=models,
            processor_list=cp.get_processors(),
            renderer=cp.get_renderer(),
            llm_service=cp.get_llm_service()
        )
    else:
        # Plain default (fast path)
        return PdfConverter(artifact_dict=models)

def _get_converter():
    global _converter
    if _converter is None:
        _converter = _build_marker_converter()
    return _converter

def _convert_with_marker(pdf_path: Path) -> tuple[str, dict, dict]:
    """
    Returns (markdown_text, images_dict, metadata_dict).
    """
    # Prefer the library text extractor that matches output_format
    try:
        from marker.output import text_from_rendered  # type: ignore
    except Exception as exc:
        raise RuntimeError(
            f"Marker is installed but internal modules are unavailable: {exc}"
        ) from exc

    converter = _get_converter()
    rendered = converter(str(pdf_path))
    text, images, metadata = text_from_rendered(rendered)
    return text, images, metadata

def _save_artifacts(out_md: Path, markdown_text: str, images: dict, metadata: Optional[dict]) -> None:
    out_md.write_text(markdown_text, encoding="utf-8")

    # Save metadata alongside as JSON
    if metadata:
        import json
        meta_path = out_md.with_name(f"{out_md.stem}_meta.json")
        meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Save extracted images (Marker returns a dict of PIL images)
    if images:
        from marker.output import convert_if_not_rgb  # type: ignore
        for name, image in images.items():
            safe = name.replace("/", "_")
            target = out_md.parent / safe
            convert_if_not_rgb(image).save(target)

def convert_one(pdf_path: Path) -> bool:
    out_md = md_for(pdf_path)
    if out_md.exists():
        LOG.info("[skip] %s -> %s (already exists)", pdf_path.name, out_md.name)
        return False
    try:
        LOG.info("[convert] %s -> %s (Marker)", pdf_path.name, out_md.name)
        markdown_text, images, metadata = _convert_with_marker(pdf_path)
        _save_artifacts(out_md, markdown_text, images, metadata)
        LOG.info("[ok]      %s", out_md)
        return True
    except Exception as e:
        LOG.error("[fail] %s: %s", pdf_path.name, e)
        return False

# --------------- runner ----------------

def initial_batch() -> int:
    count = 0
    inbox = in_dir()
    for p in sorted(inbox.iterdir()):
        if is_pdf(p):
            if convert_one(p):
                count += 1
    return count

def watch_loop() -> None:
    inbox = in_dir()
    LOG.info("\nWatching '%s' for new PDFs… (poll every %.1fs)", inbox, POLL_INTERVAL_SEC)
    seen: Set[Path] = {p.resolve() for p in inbox.iterdir() if is_pdf(p)}
    try:
        while True:
            for p in inbox.iterdir():
                if not is_pdf(p):
                    continue
                rp = p.resolve()
                # convert if it's new OR if the .md is missing
                if rp not in seen or not md_for(p).exists():
                    convert_one(p)
                    seen.add(rp)
            time.sleep(POLL_INTERVAL_SEC)
    except KeyboardInterrupt:
        LOG.info("\nStopped.")

def main() -> int:
    # Ensure dirs
    _ = in_dir()
    _ = out_dir()
    LOG.info("Input folder : %s", in_dir())
    LOG.info("Output folder: %s\n", out_dir())

    # Warm up converter so any install issues show immediately
    try:
        _ = _get_converter()
    except RuntimeError as e:
        LOG.error(str(e))
        return 1

    converted = initial_batch()
    LOG.info("Initial pass: %d file(s) converted.", converted)
    watch_loop()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
