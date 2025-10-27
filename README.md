
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
