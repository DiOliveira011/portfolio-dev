"""FastAPI app exposing the model. Docs at /docs (Swagger) and /redoc."""

from __future__ import annotations

from fastapi import FastAPI

from mlapi import __version__
from mlapi.model import service
from mlapi.schema import HealthResponse, PredictRequest, PredictResponse

app = FastAPI(
    title="ML Model API Template",
    version=__version__,
    description="Treine um modelo e sirva via API. Troque o dataset em mlapi/train.py.",
)


@app.get("/", tags=["meta"])
def root() -> dict:
    return {"name": "ML Model API Template", "docs": "/docs",
            "health": "/health", "predict": "POST /predict"}


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> dict:
    return {"status": "ok", "model_version": service.meta["model_version"]}


@app.get("/model/info", tags=["meta"])
def model_info() -> dict:
    return service.meta


@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(payload: PredictRequest) -> dict:
    return service.predict(payload.to_features())
