"""Core PDF conversion helpers built around Marker."""

from __future__ import annotations

import json
import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Optional, Union

INSTALL_HINT = "pip install marker-pdf"

LOGGER = logging.getLogger(__name__)


def is_pdf(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() == ".pdf" and not path.name.startswith(".")


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


@lru_cache(maxsize=1)
def _get_marker_converter():
    try:
        from marker.converters.pdf import PdfConverter  # type: ignore
        from marker.models import create_model_dict  # type: ignore
    except Exception as exc:  # pragma: no cover - depends on user env
        raise RuntimeError(
            f"Marker is not installed. Install it with: {INSTALL_HINT}"
        ) from exc

    models = create_model_dict()
    return PdfConverter(artifact_dict=models)


def _convert_with_marker(pdf_path: Path):
    converter = _get_marker_converter()
    rendered = converter(str(pdf_path))
    return rendered.markdown, rendered.images, rendered.metadata


def _save_artifacts(out_md: Path, markdown_text: str, images, metadata) -> None:
    out_md.write_text(markdown_text, encoding="utf-8")

    if metadata:
        meta_path = out_md.with_name(f"{out_md.stem}_meta.json")
        meta_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    if not images:
        return

    from marker.output import convert_if_not_rgb  # type: ignore

    asset_dir = out_md.with_name(f"{out_md.stem}_assets")
    asset_dir.mkdir(parents=True, exist_ok=True)

    for index, (name, image) in enumerate(images.items(), start=1):
        safe_name = name.replace("/", "_")
        unique_name = f"{out_md.stem}_{index:03d}_{safe_name}"
        target_path = asset_dir / unique_name
        convert_if_not_rgb(image).save(target_path)


def convert_pdf(pdf_path: Path, outdir: Path, *, apply_llm: bool = True, logger: Optional[logging.Logger] = None) -> bool:
    logger = logger or LOGGER
    out_md = outdir / f"{pdf_path.stem}.md"
    if out_md.exists():
        logger.info("[skip] %s already converted", pdf_path.name)
        return False

    try:
        markdown_text, images, metadata = _convert_with_marker(pdf_path)
    except RuntimeError:
        raise
    except Exception as exc:
        logger.exception("Marker failed on %s", pdf_path.name)
        raise RuntimeError(f"Marker conversion failed for {pdf_path.name}: {exc}") from exc

    cleaned = llm_cleanup(markdown_text) if apply_llm else None
    final_text = cleaned or markdown_text
    _save_artifacts(out_md, final_text, images, metadata)
    logger.info(
        "[ok] %s (%s)",
        out_md.name,
        "LLM cleanup" if cleaned else "Marker output",
    )
    return True


def llm_cleanup(md_text: str) -> Optional[str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None

    client = OpenAI(api_key=api_key)
    system_prompt = (
        "You are a meticulous Markdown and LaTeX editor. Preserve all content while fixing "
        "broken math, ensuring inline math uses $...$ and block math uses $$...$$. Merge "
        "split equations, remove stray soft hyphenation, and keep tables/lists/code blocks intact."
    )
    user_prompt = (
        "Clean the following Markdown for mathematical fidelity. Return only the corrected Markdown body.\n\n"
        f"{md_text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )
    except Exception:
        return None

    content = (response.choices[0].message.content or "").strip()
    if not content:
        return None

    if content.startswith("```)" or content.startswith("```")):
        stripped = content.strip("`").split("\n", 1)
        content = stripped[1] if len(stripped) == 2 else stripped[0]
        if content.endswith("```"):
            content = content[:-3]
    return content.strip() or None


__all__ = [
    "INSTALL_HINT",
    "convert_pdf",
    "ensure_outdir",
    "gather_inbox_pdfs",
    "is_pdf",
    "llm_cleanup",
    "resolve_pdf_paths",
]
