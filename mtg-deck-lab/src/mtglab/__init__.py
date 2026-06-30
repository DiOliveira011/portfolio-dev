"""MTG Deck Lab — Commander deck analysis and card lookup."""

from __future__ import annotations

import unicodedata

__version__ = "1.0.0"


def normalize_name(name: str) -> str:
    """Lowercase, strip accents and collapse spaces — for fuzzy name matching."""
    if not name:
        return ""
    decomposed = unicodedata.normalize("NFKD", name)
    stripped = "".join(c for c in decomposed if not unicodedata.combining(c))
    return " ".join(stripped.lower().split())
