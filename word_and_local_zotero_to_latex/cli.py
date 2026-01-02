from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from .pipeline import WordToLatex


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        "word_file",
        type=str,
        help="Path to the Word file (.docx)",
    )
    parser.add_argument(
        "--output-folder",
        type=str,
        required=True,
        help="Output folder (must be empty unless you clean it yourself)",
    )
    parser.add_argument(
        "--pandoc",
        type=str,
        default="pandoc",
        help="Pandoc executable name or full path",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Concurrent workers for fetching BibTeX",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    converter = WordToLatex(
        word_path=Path(args.word_file),
        output_folder=Path(args.output_folder),
        pandoc=args.pandoc,
        num_workers=args.workers,
        verbose=args.verbose,
    )
    converter.run()

