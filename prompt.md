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
        action="store_true",
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


## converter
"""Core PDF conversion helpers built around Marker."""

import json
import logging
import os
from dataclasses import dataclass
from functools import lru_cache
import re
from pathlib import Path
from typing import Iterable, Union

INSTALL_HINT = "pip install marker-pdf"

LOGGER = logging.getLogger(__name__)
DEFAULT_LLM_SERVICE = "pdf_converter.llm_services.LoggingGoogleGeminiService"


DEFAULT_LLM_SERVICE = "marker.services.gemini.GoogleGeminiService"


@dataclass(frozen=True)
class MarkerOptions:
    use_llm: bool = True
    # Inline math needs OCR to recover LaTeX, keep it on by default.
    force_ocr: bool = True
    redo_inline_math: bool = True

    strip_existing_ocr: bool = True
    llm_service: str | None = DEFAULT_LLM_SERVICE

    # supply via env (preferred) or here:
    gemini_api_key: str | None = None

    def to_config(self) -> dict[str, object]:
        config: dict[str, object] = {}
        if self.use_llm:
            config["use_llm"] = True
        if self.force_ocr:
            config["force_ocr"] = True
        if self.strip_existing_ocr:
            config["strip_existing_ocr"] = True
        if self.redo_inline_math:
            config["redo_inline_math"] = True
        if self.llm_service:
            config["llm_service"] = self.llm_service

        gemini_key = self.resolved_gemini_api_key()
        if gemini_key:
            config["gemini_api_key"] = gemini_key
        return config

    def describe(self) -> str:
        gemini_source = self._gemini_source()
        parts = [
            f"use_llm={self.use_llm}",
            f"force_ocr={self.force_ocr}",
            f"strip_existing_ocr={self.strip_existing_ocr}",
            f"redo_inline_math={self.redo_inline_math}",
            f"llm_service={self.llm_service or 'None'}",
            f"gemini_api_key={gemini_source}",
        ]
        return ", ".join(parts)

    def resolved_gemini_api_key(self) -> str | None:
        if self.gemini_api_key:
            return self.gemini_api_key
        return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    def _gemini_source(self) -> str:
        if self.gemini_api_key:
            return "provided"
        if os.getenv("GEMINI_API_KEY"):
            return "env:GEMINI_API_KEY"
        if os.getenv("GOOGLE_API_KEY"):
            return "env:GOOGLE_API_KEY"
        return "None"

    def label(self) -> str:
        parts: list[str] = []
        if self.use_llm:
            parts.append("use_llm")
        if self.force_ocr:
            parts.append("force_ocr")
        if self.strip_existing_ocr:
            parts.append("strip_existing_ocr")
        if self.redo_inline_math:
            parts.append("redo_inline_math")
        if self.llm_service:
            parts.append(self.llm_service.rsplit(".", 1)[-1])
        return "Marker (" + ", ".join(parts) + ")" if parts else "Marker (default)"


def is_pdf(path: Path) -> bool:
    return (
        path.is_file()
        and path.suffix.lower() == ".pdf"
        and not path.name.startswith(".")
    )


def ensure_outdir(base: Path) -> Path:
    outdir = base / "markdown"
    outdir.mkdir(parents=True, exist_ok=True)
    return outdir


def resolve_pdf_paths(argv: Iterable[Union[str, Path]]) -> list[Path]:
    seen: set[Path] = set()
    pdfs: list[Path] = []
    for raw in argv:
        path = Path(raw).expanduser()
        if not is_pdf(path):
            continue
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        pdfs.append(resolved)
    return pdfs


def gather_inbox_pdfs(inbox_dir: Path, outdir: Path) -> list[Path]:
    inbox_dir.mkdir(parents=True, exist_ok=True)
    pdfs: list[Path] = []
    for pdf in sorted(inbox_dir.glob("*.pdf")):
        if not is_pdf(pdf):
            continue
        if (outdir / f"{pdf.stem}.md").exists():
            continue
        pdfs.append(pdf.resolve())
    return pdfs


@lru_cache(maxsize=None)
def _get_marker_converter(options: MarkerOptions):
    try:
        from marker.converters.pdf import PdfConverter  # type: ignore
        from marker.models import create_model_dict  # type: ignore
        from marker.config.parser import ConfigParser  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on user env
        raise RuntimeError(
            f"Marker is not installed. Install it with: {INSTALL_HINT}"
        ) from exc

    models = create_model_dict()
    overrides = options.to_config()

    if overrides:
        config_values: dict[str, object] = {"output_format": "markdown", **overrides}
        parser = ConfigParser(config_values)
        return PdfConverter(
            config=parser.generate_config_dict(),
            artifact_dict=models,
            processor_list=parser.get_processors(),
            renderer=parser.get_renderer(),
            llm_service=parser.get_llm_service(),
        )

    return PdfConverter(artifact_dict=models)


def _convert_with_marker(pdf_path: Path, options: MarkerOptions):
    converter = _get_marker_converter(options)
    rendered = converter(str(pdf_path))
    return rendered.markdown, rendered.images, rendered.metadata


def _save_artifacts(
    out_md: Path,
    markdown_text: str,
    images,
    metadata: dict | None,
) -> None:
    """Persist Markdown, metadata, and extracted image assets."""
    path_map: dict[str, str] = {}
    final_markdown = markdown_text

    if images:
        from marker.output import convert_if_not_rgb  # type: ignore

        asset_dir = out_md.with_name(f"{out_md.stem}_assets")
        asset_dir.mkdir(parents=True, exist_ok=True)

        for index, (name, image) in enumerate(images.items(), start=1):
            safe_name = name.replace("/", "_")
            unique_name = f"{out_md.stem}_{index:03d}_{safe_name}"
            target_path = asset_dir / unique_name
            convert_if_not_rgb(image).save(target_path)
            relative_path = f"./{asset_dir.name}/{unique_name}"
            path_map[name] = relative_path
            if safe_name != name:
                path_map[safe_name] = relative_path

        final_markdown = _rewrite_image_paths(final_markdown, path_map)

    out_md.write_text(final_markdown, encoding="utf-8")

    if metadata:
        meta_path = out_md.with_name(f"{out_md.stem}_meta.json")
        meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def _rewrite_image_paths(markdown: str, mapping: dict[str, str]) -> str:
    if not mapping:
        return markdown

    pattern = re.compile(r"(!\[[^\]]*\]\()(\S+?)(\))")

    def replacer(match: re.Match[str]) -> str:
        prefix, path, suffix = match.groups()
        replacement = mapping.get(path)
        if replacement is None:
            replacement = mapping.get(path.split("/")[-1])
        if replacement is None:
            return match.group(0)
        return f"{prefix}{replacement}{suffix}"

    return pattern.sub(replacer, markdown)


def convert_pdf(
    pdf_path: Path,
    outdir: Path,
    *,
    options: MarkerOptions | None = None,
    logger: logging.Logger | None = None,
) -> bool:
    logger = logger or LOGGER
    options = options or MarkerOptions()
    out_md = outdir / f"{pdf_path.stem}.md"
    if out_md.exists():
        logger.info("[skip] %s already converted", pdf_path.name)
        return False

    logger.debug("Marker options: %s", options.describe())

    try:
        markdown_text, images, metadata = _convert_with_marker(pdf_path, options)
    except RuntimeError:
        raise
    except Exception as exc:
        logger.exception("Marker failed on %s", pdf_path.name)
        raise RuntimeError(
            f"Marker conversion failed for {pdf_path.name}: {exc}"
        ) from exc

    _save_artifacts(out_md, markdown_text, images, metadata)
    logger.info("[ok] %s (%s)", out_md.name, options.label())
    return True


__all__ = [
    "DEFAULT_LLM_SERVICE",
    "INSTALL_HINT",
    "MarkerOptions",
    "convert_pdf",
    "ensure_outdir",
    "gather_inbox_pdfs",
    "is_pdf",
    "resolve_pdf_paths",
]
