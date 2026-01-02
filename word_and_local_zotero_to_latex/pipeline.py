from __future__ import annotations

import asyncio
from pathlib import Path

from .models import ZoteroField
from .pandoc_runner import check_pandoc_installation, run_pandoc_docx_to_latex
from .tex_replace import replace_placeholders_in_tex
from .word_patch import WordCitationPatcher
from .zotero_bib import fetch_bibtex_for_titles


class WordToLatex:
    def __init__(
        self,
        *,
        word_path: Path,
        output_folder: Path,
        pandoc: str = "pandoc",
        num_workers: int = 8,
        verbose: bool = False,
    ) -> None:
        assert word_path.exists()
        output_folder.mkdir(parents=True, exist_ok=True)

        # Enforce an empty output directory to avoid mixing stale files.
        if any(output_folder.iterdir()):
            raise SystemExit(
                f"Output folder is not empty: {output_folder}\n"
                "Please choose an empty folder or enable cleaning."
            )

        self.word_path = word_path
        self.output_folder = output_folder
        self.num_workers = num_workers
        self.pandoc = pandoc
        self.verbose = verbose

    def run(self) -> None:
        fields = self.gather_fields()
        fields = self.build_bib(fields)  # updates fields with BibTeX
        self.run_pandoc()
        self.replace_placeholders_in_tex(fields)

    def gather_fields(self) -> dict[str, list[ZoteroField]]:
        patched_docx = self.output_folder / "patched.docx"
        patcher = WordCitationPatcher(
            word_path=self.word_path,
            output_docx_path=patched_docx,
        )
        return patcher.patch_to_placeholders()

    def build_bib(
        self, fields: dict[str, list[ZoteroField]]
    ) -> dict[str, list[ZoteroField]]:
        # Collect unique titles across all placeholders.
        titles_set: set[str] = set()
        for fields_list in fields.values():
            for field in fields_list:
                title = (field.payload or {}).get("title")
                if isinstance(title, str) and title:
                    titles_set.add(title)

        titles = sorted(titles_set)
        bib = asyncio.run(fetch_bibtex_for_titles(titles, workers=self.num_workers))

        refs_bib_path = self.output_folder / "refs.bib"
        with refs_bib_path.open("w", encoding="utf-8") as f:
            for title, bib_text in bib.items():
                f.write(bib_text)
                f.write("\n")

        # Fill BibTeX back to every matching field (same title may appear many times).
        for fields_list in fields.values():
            for field in fields_list:
                title = (field.payload or {}).get("title")
                if isinstance(title, str) and title in bib:
                    field.bib = bib[title]

        return fields

    def run_pandoc(self) -> None:
        figures_dir = self.output_folder / "figures"
        run_pandoc_docx_to_latex(
            docx_path=self.output_folder / "patched.docx",
            out_tex_path=self.output_folder / "output.tex",
            extract_media_dir=figures_dir,
        )

    def replace_placeholders_in_tex(self, fields: dict[str, list[ZoteroField]]) -> None:
        tex_path = self.output_folder / "output.tex"
        replaced = replace_placeholders_in_tex(
            tex_path,
            fields,
            verbose=self.verbose,
        )
        print(f"Replaced {replaced} placeholders in tex")

