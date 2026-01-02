from __future__ import annotations

import asyncio
import re

from pyzotero import zotero
from tqdm import tqdm


def get_bibtex_from_zotero(title: str) -> str:
    """
    Query local Zotero and return a BibTeX block (as text) for a title string.
    """
    zotero_client = zotero.Zotero(
        library_id="0",
        library_type="user",
        api_key=None,
        local=True,
    )
    zotero_client.add_parameters(format="bibtex", q=title)
    data = zotero_client.top()  # returns bytes
    return data.decode("utf-8")


async def fetch_bibtex_for_titles(
    titles: list[str],
    workers: int = 8,
) -> dict[str, str]:
    """
    Fetch BibTeX blocks concurrently (threaded), keyed by title.

    Note: pyzotero is synchronous; we use threads to avoid blocking.
    """
    sem = asyncio.Semaphore(max(1, int(workers)))
    results: dict[str, str] = {}

    async def _one(title: str) -> tuple[str, str]:
        async with sem:
            bib = await asyncio.to_thread(get_bibtex_from_zotero, title)
            bib = bib.strip() if isinstance(bib, str) else str(bib).strip()
            return title, bib

    tasks = [asyncio.create_task(_one(t)) for t in titles]
    for fut in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        t, bib = await fut
        if bib:
            results[t] = bib

    return results


def bibtex_first_key(bibtex: str) -> str | None:
    """Parse the first BibTeX entry key from a BibTeX block."""
    m = re.search(r"@\w+\s*\{\s*([^,\s]+)", bibtex or "")
    if not m:
        return None
    key = m.group(1).strip()
    return key or None

