"""Request/response models (Pydantic) — the API contract."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    sepal_length: float = Field(..., ge=0, le=20, examples=[5.1])
    sepal_width: float = Field(..., ge=0, le=20, examples=[3.5])
    petal_length: float = Field(..., ge=0, le=20, examples=[1.4])
    petal_width: float = Field(..., ge=0, le=20, examples=[0.2])

    def to_features(self) -> list[float]:
        return [self.sepal_length, self.sepal_width, self.petal_length, self.petal_width]


class PredictResponse(BaseModel):
    label: str
    prediction_index: int
    probabilities: dict[str, float] | None = None


class HealthResponse(BaseModel):
    status: str
    model_version: str
