"""Tests for the routing engine."""

from __future__ import annotations

from logistics.core import hhmm_to_minutes, minutes_to_hhmm
from logistics.geo import path_distance
from logistics.routing import (
    compute_route,
    optimize_sequence,
    plan,
    summarize,
    sweep_assign,
)
from logistics.sample import sample_deliveries, sample_depot, sample_vehicles


def test_time_conversions_round_trip() -> None:
    assert minutes_to_hhmm(hhmm_to_minutes("09:30")) == "09:30"
    assert hhmm_to_minutes("00:00") == 0
    assert minutes_to_hhmm(8 * 60) == "08:00"


def test_sweep_respects_capacity_and_conserves_stops() -> None:
    ds, vs, depot = sample_deliveries(), sample_vehicles(), sample_depot()
    assignment, unassigned = sweep_assign(ds, vs, depot)
    for v in vs:
        load = sum(d.volume for d in assignment[v.id])
        assert load <= v.capacity + 1e-9
    total = sum(len(assignment[v.id]) for v in vs) + len(unassigned)
    assert total == len(ds)


def test_optimize_sequence_not_worse_and_same_set() -> None:
    ds, depot = sample_deliveries()[:8], sample_depot()
    base = path_distance([(depot.lat, depot.lon)] + [(d.lat, d.lon) for d in ds])
    opt = optimize_sequence(depot, ds)
    opt_dist = path_distance([(depot.lat, depot.lon)] + [(d.lat, d.lon) for d in opt])
    assert {d.id for d in opt} == {d.id for d in ds}
    assert opt_dist <= base + 1e-9


def test_compute_route_schedule_is_monotonic() -> None:
    ds, depot = sample_deliveries()[:5], sample_depot()
    vehicle = sample_vehicles()[0]
    route = compute_route(vehicle, depot, optimize_sequence(depot, ds))
    arrivals = [s.arrival_min for s in route.stops]
    assert arrivals == sorted(arrivals)
    assert route.total_km > 0
    assert all(isinstance(s.on_time, bool) for s in route.stops)


def test_plan_covers_all_deliveries() -> None:
    ds, vs, depot = sample_deliveries(), sample_vehicles(), sample_depot()
    routes, unassigned = plan(ds, vs, depot)
    planned = sum(len(r.stops) for r in routes)
    assert planned + len(unassigned) == len(ds)
    kpis = summarize(routes, unassigned)
    assert kpis["deliveries"] == planned
    assert 0.0 <= kpis["on_time_pct"] <= 1.0
    assert kpis["total_km"] > 0
