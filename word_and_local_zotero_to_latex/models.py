from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ZoteroField:
    # English-only comments are required by project rules.
    payload_raw: str  # Raw field code text (best-effort extracted)
    payload: dict[str, Any] | None  # Parsed payload (if valid)
    bib: str | None = None  # Filled later with a BibTeX block

