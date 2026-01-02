from __future__ import annotations

import json
from ast import literal_eval
from typing import Any


ZOTERO_PREFIX = "ADDIN ZOTERO_ITEM CSL_CITATION"


def parse_zotero_code(code: str) -> dict[str, Any] | None:
    """
    Parse a Word field code for Zotero CSL_CITATION payload.

    The payload is usually JSON. In some environments it may look like a Python
    literal; we therefore try JSON first and fall back to literal_eval.
    """
    if not isinstance(code, str):
        return None

    code = code.strip()
    if not code.startswith(ZOTERO_PREFIX):
        return None

    brace = code.find("{")
    if brace < 0:
        return None

    raw = code[brace:].strip()

    # Try JSON first (most common).
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        pass

    # Fallback: best-effort Python literal parsing.
    try:
        parsed = literal_eval(raw)
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        return None

