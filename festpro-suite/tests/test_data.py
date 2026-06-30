"""Tests for the synthetic company dataset."""

from __future__ import annotations

from festpro.data import STATUSES, generate_company_data


def test_generate_company_data() -> None:
    data = generate_company_data(n_events=400, n_clients=80)
    assert len(data.events) == 400
    assert not data.inventory.empty
    assert len(data.clients) == 80

    cols = {"date", "client", "type", "region", "revenue", "cost", "status", "nps"}
    assert cols.issubset(data.events.columns)
    assert data.events["status"].isin(STATUSES).all()
    assert (data.events["revenue"] > 0).all()


def test_has_past_and_future_events() -> None:
    data = generate_company_data(n_events=600)
    assert (data.events["date"] <= data.as_of).any()   # past
    assert (data.events["date"] > data.as_of).any()    # future (agenda)
    assert (data.events["status"] == "Realizado").any()


def test_inventory_consistency() -> None:
    data = generate_company_data()
    inv = data.inventory
    assert (inv["rented"] + inv["available"] + inv["maintenance"] <= inv["total"]).all()
    assert (inv["utilization"].between(0, 1)).all()
