"""Glue between the models and the UI/simulator.

Builds neutral-venue probability functions (used by the Monte Carlo) and a
strength ranking table for display.
"""

from __future__ import annotations

import pandas as pd

from wcp.models import PoissonModel, compute_ratings, fit_poisson, win_draw_loss
from wcp.sim import ProbFn


def build_elo(results: pd.DataFrame) -> tuple[dict[str, float], ProbFn]:
    """Return Elo ratings and a neutral-venue probability function."""
    ratings = compute_ratings(results)

    def prob(a: str, b: str) -> tuple[float, float, float]:
        return win_draw_loss(ratings[a], ratings[b], home_adv=0.0)

    return ratings, prob


def build_poisson(results: pd.DataFrame) -> tuple[PoissonModel, ProbFn]:
    """Return a fitted Poisson model and a neutral-venue probability function."""
    model = fit_poisson(results)

    def prob(a: str, b: str) -> tuple[float, float, float]:
        return model.probabilities(a, b, neutral=True)

    return model, prob


def strength_ranking(results: pd.DataFrame) -> pd.DataFrame:
    """Team strength table (Elo + Poisson attack/defense), strongest first."""
    ratings = compute_ratings(results)
    model = fit_poisson(results)
    rows = [
        {
            "team": team,
            "elo": round(rating, 1),
            "ataque": round(model.attack.get(team, 1.0), 2),
            "defesa": round(model.defense.get(team, 1.0), 2),
        }
        for team, rating in ratings.items()
    ]
    return pd.DataFrame(rows).sort_values("elo", ascending=False).reset_index(drop=True)
