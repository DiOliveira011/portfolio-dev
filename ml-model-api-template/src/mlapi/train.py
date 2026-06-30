"""Train and persist the model.

This is the part you swap for your own dataset/model. The example uses the
classic Iris dataset (ships with scikit-learn — no download needed).
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

MODEL_VERSION = "1.0.0"
FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

ARTIFACT_DIR = Path(__file__).resolve().parents[2] / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "model.joblib"
META_PATH = ARTIFACT_DIR / "model_meta.json"


def load_dataset() -> tuple:
    """Return (X, y, class_names). Replace with your own loader."""
    data = load_iris()
    return data.data, data.target, list(data.target_names)


def train_model(random_state: int = 42) -> tuple[Pipeline, dict]:
    """Fit a pipeline and return (model, metadata-with-metrics)."""
    x, y, class_names = load_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=random_state, stratify=y
    )
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=random_state)),
    ])
    model.fit(x_train, y_train)
    preds = model.predict(x_test)
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, preds)), 4),
        "f1_macro": round(float(f1_score(y_test, preds, average="macro")), 4),
        "n_test": int(len(y_test)),
    }
    meta = {
        "model_version": MODEL_VERSION,
        "algorithm": "RandomForestClassifier",
        "features": FEATURES,
        "classes": class_names,
        "metrics": metrics,
        "trained_at": datetime.now(UTC).isoformat(),
    }
    return model, meta


def save_model(model: Pipeline, meta: dict,
               model_path: Path = MODEL_PATH, meta_path: Path = META_PATH) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    model, meta = train_model()
    save_model(model, meta)
    print(f"[OK] Modelo treinado e salvo em {MODEL_PATH}")
    print(f"     Metricas: {meta['metrics']}")


if __name__ == "__main__":
    main()
