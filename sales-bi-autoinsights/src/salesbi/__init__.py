"""Sales BI Auto-Insights — recebe dados de vendas e escreve os achados sozinho."""

from __future__ import annotations

__version__ = "1.0.0"
APP_TITLE = "Sales BI Auto-Insights"


def fmt_brl(valor: float) -> str:
    """Format a number as Brazilian currency: 1234567 -> 'R$ 1.234.567'."""
    return "R$ " + f"{valor:,.0f}".replace(",", ".")
