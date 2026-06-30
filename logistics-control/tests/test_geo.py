"""Tests for geographic helpers."""

from __future__ import annotations

from logistics.geo import haversine_km, path_distance


def test_haversine_zero_for_same_point() -> None:
    assert haversine_km((-23.55, -46.63), (-23.55, -46.63)) == 0.0


def test_haversine_symmetric_and_reasonable() -> None:
    a, b = (-23.5505, -46.6333), (-23.5670, -46.6680)
    assert abs(haversine_km(a, b) - haversine_km(b, a)) < 1e-9
    assert 1.0 < haversine_km(a, b) < 10.0  # a few km within São Paulo


def test_path_distance_sums_legs() -> None:
    pts = [(0.0, 0.0), (0.0, 1.0), (0.0, 2.0)]
    leg = haversine_km(pts[0], pts[1])
    assert abs(path_distance(pts) - 2 * leg) < 1e-6
