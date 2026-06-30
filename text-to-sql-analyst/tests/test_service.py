"""Tests for the analyst service (end-to-end, offline)."""

from __future__ import annotations

from t2sql.service import AnalystService

svc = AnalystService(seed=7)


def test_faturamento_total() -> None:
    out = svc.ask("faturamento total")
    assert out["ok"]
    assert out["columns"] == ["faturamento_total"]
    assert out["rows"][0][0] > 0


def test_por_mes_returns_many_rows() -> None:
    out = svc.ask("faturamento por mês")
    assert out["ok"]
    assert len(out["rows"]) >= 6  # ~12 meses de dados


def test_unknown_question() -> None:
    out = svc.ask("me conte uma piada")
    assert not out["ok"]
    assert "error" in out


def test_blank_question() -> None:
    assert not svc.ask("")["ok"]
