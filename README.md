# PDF Converter (Marker-based)

This watcher turns PDFs dropped into an inbox folder into Markdown using [Marker](https://github.com/VikParuchuri/marker). It defaults to Marker hybrid mode with Google Gemini for the highest math fidelity.

## Features
- Watches an `inbox/` folder and writes Markdown in `markdown/`
- Extracts images alongside Markdown
- Hybrid LLM mode on by default (`use_llm`, `force_ocr`, `redo_inline_math`)
- Custom Gemini service that logs the prompt being sent to Google

## Local Setup
```bash
uv sync
# Ensure .env contains GOOGLE_API_KEY=...
uv run pdf-converter-watch
```

## Install as a Library in Other Projects
You can reuse the conversion helpers directly. From another uv project:

```bash
uv add /path/to/marker-math-md
# on this machine the project lives at
uv add /your_path/marker-math-md
```

Then:

```python
from pathlib import Path
from pdf_converter.conversion import MarkerOptions, convert_pdf, ensure_outdir

options = MarkerOptions()  # already defaults to hybrid mode
output_dir = ensure_outdir(Path.cwd())
convert_pdf(Path("docs/paper.pdf"), output_dir, options=options)
```

This writes `paper.md` (plus assets) under `output_dir`. Adjust the options if you need to disable hybrid mode (`MarkerOptions(use_llm=False)`) or tweak OCR settings.

## CLI Options
```bash
uv run pdf-converter-watch --help
```

Key flags:
- `--use-llm / --no-use-llm` toggle hybrid mode
- `--force-ocr / --no-force-ocr` controls OCR for math recovery (default on)
- `--redo-inline-math / --no-redo-inline-math` re-runs inline math detection (default on)
- `--llm-service` swap to a different Marker LLM backend
- `--gemini-api-key` provide the Gemini key via CLI (defaults to `.env`)

## Environment
Create a `.env` next to the project root with:
```
GOOGLE_API_KEY=...
```

Marker also honours `GEMINI_API_KEY`. The CLI loads `.env` automatically via `python-dotenv`.
When you import the library directly, it also falls back to loading the `.env` that ships with this project (if present), so your local key is still picked up.
