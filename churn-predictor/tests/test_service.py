"""Tests for the service layer (KPIs + simulate)."""

from __future__ import annotations

from churn.service import ChurnService

svc = ChurnService(n=300, seed=42)


def test_kpis_consistent() -> None:
    k = svc.kpis()
    assert k["total"] == 300
    assert 0 <= k["em_risco"] <= k["ativos"] <= k["total"]
    assert k["receita_ativa"] >= k["receita_risco"] >= 0


def test_top_risco_sorted_desc() -> None:
    top = svc.top_risco(10)
    riscos = [c["risco"] for c in top]
    assert riscos == sorted(riscos, reverse=True)
    assert len(top) <= 10


def test_simulate_range() -> None:
    out = svc.simulate({"tenure_meses": 3, "mensalidade": 150.0, "contrato_ord": 0,
                        "suporte_chamados": 6, "atraso_pagamento": 1, "uso_gb": 30.0})
    assert 0.0 <= out["risco"] <= 1.0
    assert out["banda"] in {"Alto", "Médio", "Baixo"}
