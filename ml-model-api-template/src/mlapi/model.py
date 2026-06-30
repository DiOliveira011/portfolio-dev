"""Model service: lazily loads (or trains) the artifact and serves predictions."""

from __future__ import annotations

import json
import threading
from pathlib import Path

import joblib
import numpy as np

from mlapi.train import META_PATH, MODEL_PATH, save_model, train_model


class ModelService:
    """Loads the persisted model once; trains on first use if missing."""

    def __init__(self, model_path: Path = MODEL_PATH, meta_path: Path = META_PATH) -> None:
        self._model_path = Path(model_path)
        self._meta_path = Path(meta_path)
        self._model = None
        self._meta: dict | None = None
        self._lock = threading.Lock()

    def _ensure_loaded(self):
        if self._model is None:
            with self._lock:
                if self._model is None:
                    if not (self._model_path.exists() and self._meta_path.exists()):
                        model, meta = train_model()
                        save_model(model, meta, self._model_path, self._meta_path)
                    self._model = joblib.load(self._model_path)
                    self._meta = json.loads(self._meta_path.read_text(encoding="utf-8"))
        return self._model

    @property
    def meta(self) -> dict:
        self._ensure_loaded()
        assert self._meta is not None
        return self._meta

    def predict(self, features: list[float]) -> dict:
        model = self._ensure_loaded()
        classes = self.meta["classes"]
        x = np.asarray(features, dtype=float).reshape(1, -1)
        index = int(model.predict(x)[0])
        probabilities = None
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(x)[0]
            probabilities = {classes[i]: round(float(p), 4) for i, p in enumerate(probs)}
        return {"prediction_index": index, "label": classes[index],
                "probabilities": probabilities}


#: Module-level singleton used by the API.
service = ModelService()
