"""Tests for the seeded database."""

from __future__ import annotations

from t2sql.database import build_connection


def test_seed_counts() -> None:
    conn = build_connection(seed=7)
    assert conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0] == 12
    assert conn.execute("SELECT COUNT(*) FROM clientes").fetchone()[0] == 120
    assert conn.execute("SELECT COUNT(*) FROM vendas").fetchone()[0] == 2600


def test_revenue_positive() -> None:
    conn = build_connection(seed=7)
    total = conn.execute("SELECT SUM(valor) FROM vendas").fetchone()[0]
    assert total > 0


def test_deterministic() -> None:
    a = build_connection(seed=7).execute("SELECT SUM(valor) FROM vendas").fetchone()[0]
    b = build_connection(seed=7).execute("SELECT SUM(valor) FROM vendas").fetchone()[0]
    assert a == b
