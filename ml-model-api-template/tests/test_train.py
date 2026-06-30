"""Tests for training."""

from __future__ import annotations

from mlapi.train import FEATURES, train_model


def test_train_metrics() -> None:
    _model, meta = train_model()
    assert meta["metrics"]["accuracy"] >= 0.85
    assert meta["features"] == FEATURES
    assert len(meta["classes"]) == 3


def test_predict_setosa() -> None:
    model, meta = train_model()
    pred = model.predict([[5.1, 3.5, 1.4, 0.2]])  # pétalas pequenas → setosa
    assert meta["classes"][int(pred[0])] == "setosa"
