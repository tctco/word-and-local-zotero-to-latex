# word_and_local_zotero_to_latex

Convert a Word `.docx` with Zotero citations (Word field codes) into LaTeX, and
replace citations with `\cite{...}` keys fetched from your **local Zotero**. Currently only works on Windows.

You may need to enable Zotero local server by

<img width="1103" height="692" alt="01a4b6df11c046f4e6654e79fa5986b6" src="https://github.com/user-attachments/assets/f10c1c66-056a-4f0b-85f9-631f9d80798d" />


## Requirements

- **Windows** (uses `pywin32` to automate Microsoft Word)
- **Microsoft Word** installed
- **Zotero** installed (local library available)
- ~~**Pandoc** installed (CLI executable)~~ This should be handled by `pypandoc_binary` as you sync the venv 

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

- `output/patched.docx`: Word file with Zotero fields replaced by placeholders
- `output/output.tex`: pandoc-generated LaTeX with placeholders replaced to `\cite{...}`
- `output/refs.bib`: BibTeX entries fetched from local Zotero
- `output/figures/`: extracted media (images) from pandoc

