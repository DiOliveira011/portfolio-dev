"""Core domain: transaction model and category taxonomy."""

from __future__ import annotations

from findash.core.categories import (
    CATEGORIES,
    INCOME_CATEGORY,
    KEYWORD_RULES,
    UNCATEGORIZED,
)
from findash.core.models import Transaction, TransactionType

__all__ = [
    "CATEGORIES",
    "INCOME_CATEGORY",
    "KEYWORD_RULES",
    "UNCATEGORIZED",
    "Transaction",
    "TransactionType",
]
