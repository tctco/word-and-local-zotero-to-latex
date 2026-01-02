from __future__ import annotations

from pathlib import Path
import pypandoc


def run_pandoc_docx_to_latex(
    docx_path: Path,
    out_tex_path: Path,
    extract_media_dir: Path,
) -> None:
    extra_args = [
        "--from=docx",
        "--to=latex",
        f"--extract-media={str(extract_media_dir)}",
        "--wrap=none",
    ]
    pypandoc.convert_file(
        str(docx_path),
        to="latex",
        outputfile=str(out_tex_path),
        extra_args=extra_args,
    )