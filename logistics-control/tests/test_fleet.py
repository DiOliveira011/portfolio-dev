"""Tests for fuel costs and driver/fleet reporting."""

from __future__ import annotations

from logistics.fleet import generate_history, summarize_drivers
from logistics.routing import plan
from logistics.sample import (
    sample_deliveries,
    sample_depot,
    sample_drivers,
    sample_vehicles,
)


def test_route_fuel_cost() -> None:
    routes, _ = plan(sample_deliveries(), sample_vehicles(), sample_depot())
    route = next(r for r in routes if r.stops)
    liters = route.total_km / route.vehicle.km_per_liter
    assert abs(route.fuel_liters - liters) < 1e-9
    assert abs(route.fuel_cost(6.0) - liters * 6.0) < 1e-9


def test_generate_history_schema() -> None:
    history = generate_history(sample_drivers(), sample_vehicles(), days=20, seed=1)
    assert not history.empty
    assert {"date", "driver", "km", "fuel_liters", "fuel_cost", "deliveries"}.issubset(
        history.columns
    )
    assert (history["km"] > 0).all()
    assert (history["fuel_cost"] > 0).all()


def test_summarize_drivers_periods() -> None:
    drivers = sample_drivers()
    history = generate_history(drivers, sample_vehicles(), days=30, seed=2)
    report = summarize_drivers(history)
    assert len(report) == len(drivers)
    # Day total never exceeds week or month totals.
    assert (report["km_dia"] <= report["km_semana"] + 1e-9).all()
    assert (report["km_dia"] <= report["km_mes"] + 1e-9).all()
    assert (report["combustivel_mes"] > 0).all()
