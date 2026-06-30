"""Tests for analytics metrics."""

from __future__ import annotations

import pandas as pd

from findash.analysis import by_category, by_month, summary, top_expenses


def _df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2024-01-05", "2024-01-10", "2024-02-03", "2024-02-20"]
            ),
            "description": ["Salario", "Mercado", "Uber", "Mercado"],
            "amount": [5000.0, -200.0, -50.0, -150.0],
            "category": ["Renda", "Mercado", "Transporte", "Mercado"],
        }
    )


def test_summary() -> None:
    s = summary(_df())
    assert s.income == 5000.0
    assert s.expense == 400.0
    assert s.net == 4600.0
    assert round(s.savings_rate, 2) == 0.92
    assert s.transactions == 4
    assert s.months == 2
    assert s.avg_monthly_expense == 200.0


def test_by_category() -> None:
    cats = by_category(_df())
    # Mercado is the biggest expense category (200 + 150 = 350).
    assert cats.iloc[0]["category"] == "Mercado"
    assert cats.iloc[0]["total"] == 350.0
    assert round(cats["share"].sum(), 6) == 1.0


def test_by_month() -> None:
    months = by_month(_df())
    assert list(months["month"]) == ["2024-01", "2024-02"]
    jan = months[months["month"] == "2024-01"].iloc[0]
    assert jan["income"] == 5000.0
    assert jan["expense"] == 200.0
    assert jan["net"] == 4800.0


def test_top_expenses() -> None:
    top = top_expenses(_df(), n=2)
    assert len(top) == 2
    assert top.iloc[0]["amount"] == 200.0  # largest expense magnitude
    assert (top["amount"] > 0).all()  # magnitudes are positive
