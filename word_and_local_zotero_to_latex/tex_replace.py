from __future__ import annotations

from pathlib import Path

from .models import ZoteroField
from .zotero_bib import bibtex_first_key


def replace_placeholders_in_tex(
    tex_path: Path,
    fields_by_placeholder: dict[str, list[ZoteroField]],
    *,
    verbose: bool = False,
) -> int:
    """
    Replace placeholders in LaTeX with \\cite{...} calls.

    Returns the count of placeholders replaced (attempted).
    """
    total_replacement = 0

    text = tex_path.read_text(encoding="utf-8")

    for placeholder, fields_list in fields_by_placeholder.items():
        keys = [bibtex_first_key(field.bib or "") for field in fields_list]
        keys = [key for key in keys if key is not None]
        if len(keys) == 0:
            continue

        keys_str = ",".join(keys)
        if verbose:
            print(placeholder, keys_str)

        text = text.replace(placeholder, f"\\cite{{{keys_str}}}")
        total_replacement += 1

    tex_path.write_text(text, encoding="utf-8")
    return total_replacement

