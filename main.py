import argparse
import sys
import time
from pathlib import Path

try:
    import pymupdf4llm as pml
except Exception as exc:  # pragma: no cover - import guards are hard to test
    msg = (
        "ERROR: Failed to import pymupdf4llm. "
        "Install dependencies with 'uv add pymupdf4llm' and try again."
    )
    print(msg, file=sys.stderr)
    raise


def is_pdf(path: Path) -> bool:
    """Return True when the path points to a visible PDF file."""
    if path.name.startswith(".") or path.name.endswith("~"):
        return False
    return path.is_file() and path.suffix.lower() == ".pdf"


def convert_one(pdf_path: Path, out_dir: Path, *, force: bool = False) -> bool:
    """Convert `pdf_path` to Markdown in `out_dir`. Returns True on success."""
    md_path = out_dir / f"{pdf_path.stem}.md"
    if md_path.exists() and not force:
        print(f"[skip] {pdf_path.name} → {md_path.name} (already exists)")
        return False

    try:
        md_text = pml.to_markdown(str(pdf_path))
        md_path.write_text(md_text, encoding="utf-8")
        print(f"[ok]   {pdf_path.name} → {md_path.name}")
        return True
    except Exception as exc:  # pragma: no cover - surfaces useful failure info
        print(f"[fail] {pdf_path.name}: {exc}", file=sys.stderr)
        return False


def iter_pdfs(directory: Path) -> list[Path]:
    return [path for path in sorted(directory.iterdir()) if is_pdf(path)]


def batch_once(in_dir: Path, out_dir: Path, *, force: bool = False) -> int:
    """Convert every PDF in `in_dir` once."""
    out_dir.mkdir(parents=True, exist_ok=True)
    converted = 0
    for pdf_path in iter_pdfs(in_dir):
        if convert_one(pdf_path, out_dir, force=force):
            converted += 1
    return converted


def watch_loop(
    in_dir: Path,
    out_dir: Path,
    *,
    force: bool,
    interval: float,
) -> None:
    """Poll `in_dir` for new or updated PDFs and convert them."""
    print(f"Watching '{in_dir}' for new PDFs (poll every {interval:.1f}s). Press Ctrl+C to stop.")
    seen: dict[Path, float] = {}

    # Seed the seen cache with current files so we only process updates.
    for pdf_path in iter_pdfs(in_dir):
        try:
            seen[pdf_path.resolve()] = pdf_path.stat().st_mtime
        except FileNotFoundError:
            continue

    while True:
        try:
            for pdf_path in iter_pdfs(in_dir):
                resolved = pdf_path.resolve()
                try:
                    modified = pdf_path.stat().st_mtime
                except FileNotFoundError:
                    continue

                should_convert = resolved not in seen or modified > seen[resolved]
                if should_convert:
                    convert_one(pdf_path, out_dir, force=force)
                    seen[resolved] = modified
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nStopped watching.")
            return


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch convert PDFs to Markdown using PyMuPDF4LLM.",
    )
    parser.add_argument(
        "--in",
        dest="in_dir",
        required=True,
        help="Folder containing PDFs to convert.",
    )
    parser.add_argument(
        "--out",
        dest="out_dir",
        required=True,
        help="Destination folder for Markdown files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing Markdown files.",
    )
    parser.add_argument(
        "--no-watch",
        action="store_true",
        help="Only run a single batch conversion and exit.",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=3.0,
        help="Polling interval in seconds when watching for updates (default: 3).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    in_dir = Path(args.in_dir).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()

    if not in_dir.exists() or not in_dir.is_dir():
        print(f"ERROR: Input directory does not exist or is not a directory: {in_dir}", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    converted = batch_once(in_dir, out_dir, force=args.force)
    print(f"Initial pass converted {converted} file(s).")

    if not args.no_watch:
        watch_loop(in_dir, out_dir, force=args.force, interval=args.interval)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
