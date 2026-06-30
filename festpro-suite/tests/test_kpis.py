"""Tests for KPI calculations."""

from __future__ import annotations

from festpro import kpis
from festpro.data import generate_company_data


def test_overview_ranges() -> None:
    data = generate_company_data()
    o = kpis.overview(data)
    assert o.revenue_month >= 0
    assert 0.0 <= o.conversion <= 1.0
    assert 0.0 <= o.inventory_util <= 1.0
    assert 0.0 <= o.on_time <= 1.0
    assert o.receivables >= 0


def test_revenue_by_month_sorted_and_capped() -> None:
    data = generate_company_data()
    rev = kpis.revenue_by_month(data.events, months=12)
    assert len(rev) <= 12
    assert list(rev["month"]) == sorted(rev["month"])
    assert (rev["revenue"] >= 0).all()


def test_by_type_matches_realized_total() -> None:
    data = generate_company_data()
    total_realized = kpis.realized(data.events)["revenue"].sum()
    assert abs(kpis.by_type(data.events)["receita"].sum() - total_realized) < 1.0


def test_funnel_is_monotonic() -> None:
    data = generate_company_data()
    fun = kpis.funnel(data.events, data.as_of).set_index("etapa")["quantidade"]
    assert fun["Orçamentos"] >= fun["Confirmados"] >= fun["Realizados"]


def test_receivables_and_drivers() -> None:
    data = generate_company_data()
    aging = kpis.receivables_aging(data.events, data.as_of)
    assert (aging["valor"] >= 0).all()
    drv = kpis.deliveries_by_driver(data.events)
    assert (drv["no_prazo"].between(0, 1)).all()
    assert (drv["km"] > 0).all()
