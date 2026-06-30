"""Strength models: Elo ratings and an independent-Poisson goals model."""

from __future__ import annotations

from wcp.models.elo import compute_ratings, win_draw_loss
from wcp.models.poisson import PoissonModel, fit_poisson

__all__ = ["compute_ratings", "win_draw_loss", "PoissonModel", "fit_poisson"]
