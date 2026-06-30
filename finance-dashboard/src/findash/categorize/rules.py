"""Keyword-based categorization rules."""

from __future__ import annotations

from findash.core.categories import INCOME_CATEGORY, KEYWORD_RULES
from findash.utils.formatting import normalize_text

# Expense categories, in priority order (income handled separately).
_EXPENSE_RULES: list[tuple[str, list[str]]] = [
    (category, keywords)
    for category, keywords in KEYWORD_RULES.items()
    if category != INCOME_CATEGORY
]
_INCOME_KEYWORDS = KEYWORD_RULES[INCOME_CATEGORY]


def categorize_by_rules(description: str, amount: float) -> str | None:
    """Return a category from keyword rules, or ``None`` if undecided.

    Positive amounts are treated as income unless they clearly match a specific
    category (e.g. an investment redemption). Negative amounts try the expense
    keyword rules and return ``None`` when nothing matches.
    """
    norm = normalize_text(description)

    if amount >= 0:
        if _matches(norm, _INCOME_KEYWORDS):
            return INCOME_CATEGORY
        for category, keywords in _EXPENSE_RULES:
            if category in ("Transferências", "Investimentos") and _matches(norm, keywords):
                return category
        return INCOME_CATEGORY

    for category, keywords in _EXPENSE_RULES:
        if _matches(norm, keywords):
            return category
    return None


def _matches(normalized_text: str, keywords: list[str]) -> bool:
    return any(keyword in normalized_text for keyword in keywords)
