"""Tests for the FastAPI endpoints."""

from __future__ import annotations

from fastapi.testclient import TestClient

from mlapi.api import app

client = TestClient(app)

_SETOSA = {"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}


def test_health() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_model_info() -> None:
    r = client.get("/model/info")
    assert r.status_code == 200
    body = r.json()
    assert "features" in body and "metrics" in body


def test_predict_setosa() -> None:
    r = client.post("/predict", json=_SETOSA)
    assert r.status_code == 200
    body = r.json()
    assert body["label"] == "setosa"
    assert body["probabilities"]["setosa"] > 0.5


def test_validation_rejects_bad_payload() -> None:
    r = client.post("/predict", json={"sepal_length": -1})
    assert r.status_code == 422
