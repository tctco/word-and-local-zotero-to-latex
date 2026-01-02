from __future__ import annotations

import re


def make_citation_placeholder(citation_id: str) -> str:
    """
    Create a pandoc-safe placeholder string.

    We intentionally avoid underscores and other punctuation that pandoc may escape.
    """
    cid = re.sub(r"[^A-Za-z0-9]+", "", citation_id or "")
    if not cid:
        cid = "X"
    return f"ZCIT{cid}Z"

