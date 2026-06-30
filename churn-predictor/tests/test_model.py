"""Tests for training and scoring."""

from __future__ import annotations

from churn.data import generate_customers
from churn.model import risk_band, score_one, train

_HIGH = {"tenure_meses": 2, "mensalidade": 160.0, "contrato_ord": 0,
         "suporte_chamados": 8, "atraso_pagamento": 1, "uso_gb": 25.0}
_LOW = {"tenure_meses": 60, "mensalidade": 60.0, "contrato_ord": 2,
        "suporte_chamados": 0, "atraso_pagamento": 0, "uso_gb": 25.0}


def _model():
    return train(generate_customers(n=800, seed=42), seed=42)


def test_model_learns_signal() -> None:
    out = _model()
    assert out["metrics"]["roc_auc"] > 0.75


def test_importances_sum_to_one() -> None:
    out = _model()
    total = sum(i["peso"] for i in out["importances"])
    assert abs(total - 1.0) < 0.02


def test_high_risk_scores_higher() -> None:
    model = _model()["model"]
    assert score_one(model, _HIGH) > score_one(model, _LOW)


def test_risk_band() -> None:
    assert risk_band(0.9) == "Alto"
    assert risk_band(0.45) == "Médio"
    assert risk_band(0.1) == "Baixo"
