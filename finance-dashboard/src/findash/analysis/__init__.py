"""Analytics: KPIs and aggregations over categorized transactions."""

from __future__ import annotations

from findash.analysis.metrics import (
    Summary,
    by_category,
    by_month,
    summary,
    top_expenses,
)

__all__ = ["Summary", "by_category", "by_month", "summary", "top_expenses"]
