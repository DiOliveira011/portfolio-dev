"""Tests for aggregations and the auto-insight engine."""

from __future__ import annotations

from salesbi.data import generate_sales
from salesbi.insights import by_dimension, generate_insights, kpis, total_revenue

DATA = generate_sales(seed=11)


def test_by_dimension_sums_match_total() -> None:
    total = total_revenue(DATA)
    soma_cat = sum(by_dimension(DATA, "categoria").values())
    soma_reg = sum(by_dimension(DATA, "regiao").values())
    assert abs(soma_cat - total) < 1.0
    assert abs(soma_reg - total) < 1.0


def test_kpis_leaders_and_growth() -> None:
    k = kpis(DATA)
    assert k["categoria_lider"] == "Eletrônicos"   # 40% share
    assert k["regiao_lider"] == "Sudeste"          # 45% share
    assert k["crescimento"] > 0                    # tendência de alta


def test_insights_are_generated() -> None:
    bullets = generate_insights(DATA)
    assert len(bullets) >= 5
    assert "faturamento" in bullets[0].lower()
    assert any("ascensão" in b or "retração" in b for b in bullets)
