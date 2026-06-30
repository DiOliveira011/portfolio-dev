"""Tests for synthetic sales data."""

from __future__ import annotations

from salesbi.data import CATEGORIAS, REGIOES, generate_sales, month_labels


def test_month_labels() -> None:
    labels = month_labels(18)
    assert labels[0] == "2025-01"
    assert labels[-1] == "2026-06"
    assert len(labels) == 18


def test_shape_and_determinism() -> None:
    a = generate_sales(seed=11)
    b = generate_sales(seed=11)
    assert len(a) == 18 * len(CATEGORIAS) * len(REGIOES) * 3  # 3 canais
    assert a[0] == b[0]
    assert sum(r["valor"] for r in a) > 0
