"""Elo rating model.

Ratings update chronologically after each match; ``win_draw_loss`` turns a
rating gap into win/draw/loss probabilities with a simple draw heuristic.
"""

from __future__ import annotations

import pandas as pd

BASE = 1500.0
K = 24.0
HOME_ADV = 60.0


def compute_ratings(
    results: pd.DataFrame, *, k: float = K, base: float = BASE, home_adv: float = HOME_ADV
) -> dict[str, float]:
    """Return final Elo ratings per team from a results history."""
    ratings: dict[str, float] = {}
    df = results.sort_values("date") if "date" in results.columns else results
    for row in df.itertuples(index=False):
        ra = ratings.setdefault(row.home, base)
        rb = ratings.setdefault(row.away, base)
        exp_home = 1.0 / (1.0 + 10 ** (-((ra + home_adv) - rb) / 400.0))
        if row.home_goals > row.away_goals:
            score = 1.0
        elif row.home_goals == row.away_goals:
            score = 0.5
        else:
            score = 0.0
        ratings[row.home] = ra + k * (score - exp_home)
        ratings[row.away] = rb + k * ((1.0 - score) - (1.0 - exp_home))
    return ratings


def win_draw_loss(
    rating_a: float, rating_b: float, *, home_adv: float = 0.0, draw_factor: float = 0.27
) -> tuple[float, float, float]:
    """Probabilities (A wins, draw, B wins) from two ratings.

    The draw probability peaks when the teams are evenly matched and shrinks as
    the gap widens.
    """
    exp_a = 1.0 / (1.0 + 10 ** (-((rating_a + home_adv) - rating_b) / 400.0))
    p_draw = max(0.0, min(draw_factor * (1.0 - 2.0 * abs(exp_a - 0.5)), 0.5))
    p_a = max(0.0, exp_a - p_draw / 2.0)
    p_b = max(0.0, (1.0 - exp_a) - p_draw / 2.0)
    total = p_a + p_draw + p_b
    return (p_a / total, p_draw / total, p_b / total)
