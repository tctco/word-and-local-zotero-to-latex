# word_and_local_zotero_to_latex

Convert a Word `.docx` with Zotero citations (Word field codes) into LaTeX, and
replace citations with `\cite{...}` keys fetched from your **local Zotero**. Currently only works on Windows.

## Requirements

- **Windows** (uses `pywin32` to automate Microsoft Word)
- **Microsoft Word** installed
- **Zotero** installed (local library available)
- **Pandoc** installed (CLI executable)

## Install (uv)

This project is managed by `uv`.

```bash
uv sync
```

## Usage


Custom output folder:

```bash
uv run python main.py "path/to/input.docx" --output-folder "output"
```


## Outputs

By default, files are written to `./output/`:

- `output/patched.docx`: Word file with Zotero fields replaced by placeholders
- `output/output.tex`: pandoc-generated LaTeX with placeholders replaced to `\cite{...}`
- `output/refs.bib`: BibTeX entries fetched from local Zotero
- `output/figures/`: extracted media (images) from pandoc

