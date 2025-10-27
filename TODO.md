# Create a single-file "best tools" converter:
# - Uses Marker locally for PDF→Markdown (great math fidelity)
# - If OPENAI_API_KEY is present, runs an LLM cleanup pass to fix equations/LaTeX/structure
# - No arguments. Drag-and-drop or double-click to choose files. Outputs to ./markdown
# - Still zero config besides `pip install marker-pdf openai` and setting OPENAI_API_KEY for the optional step
from pathlib import Path
import textwrap

proj = Path("/mnt/data/pdf2md_best_plus")
proj.mkdir(parents=True, exist_ok=True)

script_path = proj / "pdf2md_best_plus.py"
script_path.write_text(textwrap.dedent("""
    #!/usr/bin/env python3
    # -*- coding: utf-8 -*-
    \"\"\"
    Best-math PDF → Markdown with optional LLM cleanup (zero-argument tool).

    How it works
    ------------
    1) Converts PDFs to Markdown using Marker (local; no network; great at equations/tables).
    2) If OPENAI_API_KEY is set, runs an LLM post-pass to normalize/fix LaTeX and structure.
       - Uses the OpenAI Chat Completions API via the `openai` Python client.
       - If the key is missing or any error occurs, it simply keeps the Marker output.

    Usage (no flags):
      - Double-click to run → file dialog → pick one or more PDFs → outputs to ./markdown
      - OR drag & drop PDFs onto this script → converts immediately to ./markdown

    Install once:
      pip install marker-pdf openai

    Set API key (optional, only for the cleanup step):
      export OPENAI_API_KEY=sk-...        # macOS/Linux
      setx OPENAI_API_KEY sk-...          # Windows (new shell)

    \"\"\"
    import os
    import sys
    import shutil
    import subprocess
    from pathlib import Path
    from typing import List, Optional

    # --- File picking (GUI if no args) ---
    def pick_pdfs_gui() -> List[Path]:
        try:
            import tkinter as tk
            from tkinter import filedialog
        except Exception:
            return []
        root = tk.Tk()
        root.withdraw()
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        try:
            root.destroy()
        except Exception:
            pass
        return [Path(f) for f in (files or [])]

    def is_pdf(p: Path) -> bool:
        return p.is_file() and p.suffix.lower() == ".pdf" and not p.name.startswith(".")

    def ensure_outdir(base: Path) -> Path:
        outdir = base / "markdown"
        outdir.mkdir(parents=True, exist_ok=True)
        return outdir

    # --- Conversion: Marker (local) ---
    def convert_with_marker(pdf_path: Path, out_md: Path) -> None:
        exe = shutil.which("marker")
        if exe:
            cmd = [exe, "--pdf", str(pdf_path), "--md", str(out_md)]
        else:
            # Fallback: python -m marker
            try:
                import marker  # noqa: F401
                cmd = [sys.executable, "-m", "marker", "--pdf", str(pdf_path), "--md", str(out_md)]
            except Exception:
                raise RuntimeError(\"Marker not installed. Install with: pip install marker-pdf\")
        subprocess.run(cmd, check=True)

    # --- Optional LLM cleanup (OpenAI) ---
    def llm_cleanup(md_text: str) -> Optional[str]:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return None
        try:
            # Minimal dependency on the official OpenAI client
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            system = (
                "You are a strict Markdown + LaTeX typesetting assistant. "
                "Your task is to clean and normalize Markdown containing math. "
                "Rules: "
                "1) Preserve meaning and all content; do not summarize or omit sections. "
                "2) Fix broken or split equations; ensure proper LaTeX syntax. "
                "3) Convert pseudo-math to LaTeX where obvious; keep inline math in $...$ and display math in $$...$$. "
                "4) Merge line-broken equations; remove soft hyphens from wrapped math tokens. "
                "5) Keep code blocks, tables, lists intact; do not hallucinate figures or citations. "
                "6) If unsure, leave text untouched. "
            )
            user = (
                "Clean this Markdown for math fidelity. "
                "Return ONLY the corrected Markdown body, no explanations:\n\n"
                f"{md_text}"
            )
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                temperature=0.0,
            )
            out = resp.choices[0].message.content or ""
            # Some clients may wrap in triple backticks; strip if present.
            if out.strip().startswith("```"):
                # naive fence strip
                out = out.strip().strip("`")
                # in case of ```markdown fences
                out = out.split("\\n", 1)[-1]
                if out.endswith("```"):
                    out = out[:-3]
            return out.strip() or None
        except Exception:
            # Any failure: fall back silently
            return None

    def main() -> int:
        # Collect PDFs
        argv_paths = [Path(a) for a in sys.argv[1:]]
        pdfs = [p for p in argv_paths if is_pdf(p)]
        if not pdfs:
            pdfs = [p for p in pick_pdfs_gui() if is_pdf(p)]
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
                    print(f"[ok] {out_md.name} (kept Marker output)")
                converted += 1
            except subprocess.CalledProcessError as e:
                print(f"[fail] {pdf.name}: converter error: {e}")
            except Exception as e:
                print(f"[fail] {pdf.name}: {e}")

        print(f\"\\nDone. Converted {converted} file(s) → {outdir}\\n\")
        return 0

    if __name__ == "__main__":
        raise SystemExit(main())
"""), encoding="utf-8")

readme_path = proj / "README.txt"
readme_path.write_text(textwrap.dedent("""
    BEST setup (math-first) — Marker + optional LLM cleanup

    1) Install:
         pip install marker-pdf openai

    2) (Optional) Set API key for cleanup:
         export OPENAI_API_KEY=sk-...        # macOS/Linux
         setx OPENAI_API_KEY sk-...          # Windows (then open a new shell)

    3) Use (no flags needed):
         - Double-click pdf2md_best_plus.py and pick PDFs, or
         - Drag & drop PDFs onto pdf2md_best_plus.py

       Outputs .md files into a 'markdown' folder next to the script.

    Notes:
      - Marker runs fully local and preserves math well.
      - If OPENAI_API_KEY is set, a second pass fixes broken LaTeX and formatting.
      - If the key is missing or the request fails, Marker output is kept as-is.
"""), encoding="utf-8")

proj, [p.name for p in proj.iterdir()]



Awesome — I’ve bundled a “**best tools**” version that uses **Marker** for the local PDF→Markdown pass *and* (if you set your API key) an **LLM cleanup** pass to fix math/LaTeX.

**Download:**

* [pdf2md_best_plus.py](sandbox:/mnt/data/pdf2md_best_plus/pdf2md_best_plus.py)
* [README.txt](sandbox:/mnt/data/pdf2md_best_plus/README.txt)

### One-time install

```bash
pip install marker-pdf openai
```

### (Optional) enable the LLM pass

```bash
# macOS/Linux
export OPENAI_API_KEY=sk-...

# Windows (new shell afterwards)
setx OPENAI_API_KEY sk-...
```

### Use (no args):

* **Double-click** `pdf2md_best_plus.py` and choose PDFs in the dialog, or
* **Drag & drop PDFs** onto the script.

Output `.md` files land in a `markdown/` folder next to the script.

**What it does**

1. Runs **Marker** locally — best-in-class at preserving equations/tables as Markdown + LaTeX.
2. If `OPENAI_API_KEY` is present, it automatically runs a **post-cleaning pass** (OpenAI Chat Completions; model set to a fast 4o-mini variant) to:

   * merge broken math lines,
   * normalize `$$...$$` display blocks and `$...$` inline math,
   * fix obvious LaTeX tokenization glitches,
   * leave everything else intact.

If the key isn’t set or the call fails, it just keeps the Marker output. No switches, no prompts — purely automatic.
