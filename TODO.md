# Create a ready-to-run batch converter for PDFs -> Markdown using PyMuPDF4LLM.
# It supports:
# - One-off batch conversion of a folder
# - Optional --watch mode that polls for new PDFs
# - Skips already-converted files unless --force is set
# - Clean logging and simple CLI
#
# It does NOT require an OpenAI key. (You can add LLM-based OCR later if you want.)

from pathlib import Path
import textwrap

project_dir = Path("/mnt/data/pdf2md_tool")
project_dir.mkdir(parents=True, exist_ok=True)

# Script file
script = project_dir / "pdf2md_batch.py"
script.write_text(textwrap.dedent("""
    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    \"\"\"
    PDF → Markdown batch converter (local, free, open-source) using PyMuPDF4LLM.

    Usage:
      # One-off batch conversion
      python pdf2md_batch.py --in ./inbox --out ./markdown

      # Watch a folder for new PDFs (polling every 3s)
      python pdf2md_batch.py --in ./inbox --out ./markdown --watch --interval 3

      # Overwrite existing .md files
      python pdf2md_batch.py --in ./inbox --out ./markdown --force

    Requirements:
      pip install pymupdf4llm

    Notes:
      - Runs fully local. No API keys needed.
      - Produces one .md per .pdf with same basename.
      - Hidden/temp files and non-PDFs are ignored.
    \"\"\"

    import argparse
    import sys
    import time
    from pathlib import Path

    try:
        import pymupdf4llm as pml
    except Exception as e:
        print("ERROR: pymupdf4llm is not installed. Install with: pip install pymupdf4llm", file=sys.stderr)
        raise

    def is_pdf(path: Path) -> bool:
        name = path.name
        if name.startswith('.') or name.endswith('~'):
            return False
        return path.is_file() and path.suffix.lower() == '.pdf'

    def convert_one(pdf_path: Path, out_dir: Path, force: bool = False) -> bool:
        md_path = out_dir / (pdf_path.stem + ".md")
        if md_path.exists() and not force:
            print(f"[skip] {pdf_path.name} → {md_path.name} (already exists)")
            return False
        try:
            md_text = pml.to_markdown(str(pdf_path))
            md_path.write_text(md_text, encoding="utf-8")
            print(f"[ok]   {pdf_path.name} → {md_path.name}")
            return True
        except Exception as e:
            print(f"[fail] {pdf_path.name}: {e}", file=sys.stderr)
            return False

    def batch_once(in_dir: Path, out_dir: Path, force: bool = False) -> int:
        out_dir.mkdir(parents=True, exist_ok=True)
        count = 0
        for pdf in sorted(in_dir.iterdir()):
            if is_pdf(pdf):
                if convert_one(pdf, out_dir, force=force):
                    count += 1
        return count

    def watch_loop(in_dir: Path, out_dir: Path, force: bool, interval: float) -> None:
        print(f"Watching '{in_dir}' for new PDFs… (poll every {interval:.1f}s)")
        seen = set()
        # Pre-populate with existing files so we only process new ones
        for pdf in in_dir.iterdir():
            if is_pdf(pdf):
                seen.add(pdf.resolve())

        while True:
            try:
                for pdf in in_dir.iterdir():
                    if not is_pdf(pdf):
                        continue
                    r = pdf.resolve()
                    if r not in seen:
                        convert_one(pdf, out_dir, force=force)
                        seen.add(r)
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\\nStopped watching.")
                return

    def parse_args(argv=None):
        ap = argparse.ArgumentParser(description="Batch convert PDFs to Markdown (local) using PyMuPDF4LLM.")
        ap.add_argument("--in", dest="in_dir", required=True, help="Input folder to scan for PDFs.")
        ap.add_argument("--out", dest="out_dir", required=True, help="Output folder for .md files.")
        ap.add_argument("--force", action="store_true", help="Overwrite .md files if they already exist.")
        ap.add_argument("--watch", action="store_true", help="Keep running and convert new PDFs as they appear.")
        ap.add_argument("--interval", type=float, default=3.0, help="Polling interval (seconds) in --watch mode.")
        return ap.parse_args(argv)

    def main(argv=None):
        args = parse_args(argv)
        in_dir = Path(args.in_dir).expanduser().resolve()
        out_dir = Path(args.out_dir).expanduser().resolve()

        if not in_dir.exists() or not in_dir.is_dir():
            print(f"ERROR: Input directory does not exist or is not a directory: {in_dir}", file=sys.stderr)
            return 2

        out_dir.mkdir(parents=True, exist_ok=True)

        # One-off batch pass
        converted = batch_once(in_dir, out_dir, force=args.force)
        print(f"Initial pass: {converted} file(s) converted.")

        # Optionally stay alive and watch for new PDFs
        if args.watch:
            watch_loop(in_dir, out_dir, force=args.force, interval=args.interval)

        return 0

    if __name__ == "__main__":
        raise SystemExit(main())
"""), encoding="utf-8")

# requirements.txt
reqs = project_dir / "requirements.txt"
reqs.write_text("pymupdf4llm>=0.0.17\n", encoding="utf-8")

# README.md with quickstart
readme = project_dir / "README.md"
readme.write_text(textwrap.dedent("""
    # PDF → Markdown (Local) with PyMuPDF4LLM

    ## Quickstart
    ```bash
    # 1) Create two folders
    mkdir -p inbox markdown

    # 2) Install dependency (only needs Python 3.9+)
    pip install -r requirements.txt
    # or: pip install pymupdf4llm

    # 3) Run a one-off batch
    python pdf2md_batch.py --in ./inbox --out ./markdown

    # 4) Or keep it running and drop PDFs into `inbox`
    python pdf2md_batch.py --in ./inbox --out ./markdown --watch --interval 3
    ```

    - Each `file.pdf` in `inbox` becomes `file.md` in `markdown`.
    - Re-run with `--force` to overwrite existing `.md` files.
    - No API keys or internet required. Everything is processed locally.
    - Works great on macOS (Intel/Apple Silicon), Linux, Windows.

    ## Why PyMuPDF4LLM?
    - Strong reading order, headings, lists, tables → clean Markdown.
    - Tiny footprint, very fast.
    - Easy to script for batch jobs.
"""), encoding="utf-8")

project_dir, list(project_dir.iterdir())
