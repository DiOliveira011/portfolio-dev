"""Text normalization and currency formatting helpers."""

from __future__ import annotations

import re
import unicodedata

_WHITESPACE = re.compile(r"\s+")


def normalize_text(text: str) -> str:
    """Lowercase, strip accents and collapse whitespace.

    Used so keyword rules and the ML classifier match regardless of accents or
    casing (e.g. ``"Padaria São João"`` -> ``"padaria sao joao"``).
    """
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFKD", text)
    no_accents = "".join(c for c in decomposed if not unicodedata.combining(c))
    return _WHITESPACE.sub(" ", no_accents.lower()).strip()


def format_currency(value: float, symbol: str = "R$") -> str:
    """Format a number as Brazilian-style currency, e.g. ``"R$ 1.234,56"``."""
    sign = "-" if value < 0 else ""
    formatted = f"{abs(value):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    return f"{sign}{symbol} {formatted}"
