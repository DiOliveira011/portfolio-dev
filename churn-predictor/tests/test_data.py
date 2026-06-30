"""Tests for the synthetic customer base."""

from __future__ import annotations

from churn.data import FEATURES, generate_customers, to_xy


def test_deterministic() -> None:
    a = generate_customers(n=200, seed=7)
    b = generate_customers(n=200, seed=7)
    assert a[0] == b[0]
    assert [c["id"] for c in a] == [c["id"] for c in b]


def test_churn_rate_plausible() -> None:
    custs = generate_customers(n=800, seed=42)
    rate = sum(c["churn"] for c in custs) / len(custs)
    assert 0.1 < rate < 0.6


def test_to_xy_shapes() -> None:
    custs = generate_customers(n=120, seed=1)
    x, y = to_xy(custs)
    assert x.shape == (120, len(FEATURES))
    assert y.shape == (120,)
