"""Train the churn model and score customers."""

from __future__ import annotations

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

from churn.data import FEATURE_LABELS, FEATURES, to_xy


def train(customers: list[dict], seed: int = 42) -> dict:
    """Fit a RandomForest and return model + metrics + feature importances."""
    x, y = to_xy(customers)
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=seed, stratify=y
    )
    model = RandomForestClassifier(
        n_estimators=300, max_depth=10, min_samples_leaf=5, random_state=seed
    )
    model.fit(x_train, y_train)

    proba = model.predict_proba(x_test)[:, 1]
    preds = (proba >= 0.5).astype(int)
    metrics = {
        "roc_auc": round(float(roc_auc_score(y_test, proba)), 3),
        "accuracy": round(float(accuracy_score(y_test, preds)), 3),
        "n_treino": int(len(y_train)),
        "n_teste": int(len(y_test)),
    }
    importances = sorted(
        ({"feature": FEATURE_LABELS[f], "peso": round(float(w), 3)}
         for f, w in zip(FEATURES, model.feature_importances_, strict=True)),
        key=lambda d: d["peso"], reverse=True,
    )
    return {"model": model, "metrics": metrics, "importances": importances}


def score_one(model: RandomForestClassifier, customer: dict) -> float:
    """Return churn probability (0..1) for a single customer dict."""
    x = np.array([[customer[f] for f in FEATURES]], dtype=float)
    return float(model.predict_proba(x)[0, 1])


def risk_band(prob: float) -> str:
    if prob >= 0.6:
        return "Alto"
    if prob >= 0.3:
        return "Médio"
    return "Baixo"
