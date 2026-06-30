"""Best-effort importer for a deck **link** (e.g. LigaMagic).

We fetch the page and try to extract a plain decklist (``"<qty> <card>"`` lines).
Deck-site HTML changes often, so this degrades gracefully: if it can't find a
list, it raises and the UI tells the user to paste the txt list instead.
"""

from __future__ import annotations

import re

import requests

_HEADERS = {"User-Agent": "Mozilla/5.0 (mtglab)"}
_LINE = re.compile(r"^\s*\d+\s*[xX]?\s+[A-Za-zÀ-ÿ].{1,80}$")


def decklist_text_from_url(url: str, *, timeout: float = 20.0) -> str:
    """Return a decklist as text extracted from ``url`` (best effort)."""
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("URL inválida.")
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=timeout)
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"Não consegui acessar o link: {exc}") from exc

    html = resp.text
    text = _extract(html)
    if text:
        return text
    raise ValueError(
        "Não consegui ler a lista de cartas desse link. "
        "Abra o deck, copie a lista (formato '1 Nome da Carta') e cole no campo de texto."
    )


def _extract(html: str) -> str | None:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # Strategy A: an export <textarea> already holding the list.
    for area in soup.find_all("textarea"):
        block = _filter_list_lines(area.get_text("\n"))
        if block:
            return block

    # Strategy B: a contiguous block of "<qty> <card>" lines anywhere in the text.
    block = _filter_list_lines(soup.get_text("\n"))
    return block


def _filter_list_lines(text: str) -> str | None:
    lines = [ln.strip() for ln in text.splitlines()]
    keep = [ln for ln in lines if _LINE.match(ln)]
    # Require a believable deck size to avoid false positives.
    return "\n".join(keep) if len(keep) >= 15 else None
