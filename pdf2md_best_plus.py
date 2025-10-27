#!/usr/bin/env python3
"""Zero-config PDF→Markdown converter with optional LLM cleanup."""

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Optional, Union

INSTALL_HINT = "pip install marker-pdf"


def pick_pdfs_gui() -> list[Path]:
    """Open a Tk file dialog when no CLI arguments are provided."""
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return []

    try:
        root = tk.Tk()
    except Exception:
        return []
    root.withdraw()
    files = filedialog.askopenfilenames(
        title="Select PDF files",
        filetypes=[("PDF files", "*.pdf")],
    )
    try:
        root.destroy()
    except Exception:
        pass
    return [Path(f) for f in files or ()]


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


def convert_with_marker(pdf_path: Path, out_md: Path) -> None:
    """Invoke Marker via CLI or python -m marker."""
    marker_exe = shutil.which("marker")
    if marker_exe:
        cmd = [marker_exe, "--pdf", str(pdf_path), "--md", str(out_md)]
    else:
        try:
            import marker  # noqa: F401  # type: ignore
        except Exception as exc:  # pragma: no cover - user environment
            raise RuntimeError(
                f"Marker is not installed. Install it with: {INSTALL_HINT}"
            ) from exc
        cmd = [
            sys.executable,
            "-m",
            "marker",
            "--pdf",
            str(pdf_path),
            "--md",
            str(out_md),
        ]
    subprocess.run(cmd, check=True)


def llm_cleanup(md_text: str) -> Optional[str]:
    """If OPENAI_API_KEY is set and client available, clean the Markdown."""
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


def main() -> int:
    argv_pdfs = resolve_pdf_paths(sys.argv[1:])
    pdfs = argv_pdfs or resolve_pdf_paths(pick_pdfs_gui())

    if not pdfs:
        print("No PDFs provided. Exiting.")
        return 0

    base_dir = Path(__file__).resolve().parent
    outdir = ensure_outdir(base_dir)
    converted = 0

    for pdf in pdfs:
        out_md = outdir / (pdf.stem + ".md")
        try:
            print(f"[convert] {pdf.name} -> {out_md.name} (Marker)")
            convert_with_marker(pdf, out_md)
            md_text = out_md.read_text(encoding="utf-8")
            cleaned = llm_cleanup(md_text)
            if cleaned:
                out_md.write_text(cleaned, encoding="utf-8")
                print(f"[ok] {out_md.name} (LLM cleanup applied)")
            else:
                print(f"[ok] {out_md.name} (Marker output)")
            converted += 1
        except subprocess.CalledProcessError as err:
            print(f"[fail] {pdf.name}: Marker conversion error: {err}")
        except RuntimeError as err:
            print(err)
            return 1
        except Exception as err:
            print(f"[fail] {pdf.name}: {err}")

    print(f"\nDone. Converted {converted} file(s) to: {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
