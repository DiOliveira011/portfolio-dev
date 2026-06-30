"""Independent-Poisson goals model (attack x defense strengths).

Each team gets an ``attack`` and ``defense`` factor relative to the league
average. Expected goals for a match combine the home team's attack with the away
team's defense (and vice-versa); scoreline probabilities follow two independent
Poisson distributions.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class PoissonModel:
    """Fitted attack/defense strengths plus league baselines."""

    attack: dict[str, float]
    defense: dict[str, float]
    mu: float          # average goals per team per game
    home_adj: float    # home-goals multiplier (> 1 means home advantage)
    away_adj: float

    def expected_goals(
        self, home: str, away: str, *, neutral: bool = False
    ) -> tuple[float, float]:
        ha = 1.0 if neutral else self.home_adj
        aa = 1.0 if neutral else self.away_adj
        eh = self.mu * self.attack[home] * self.defense[away] * ha
        ea = self.mu * self.attack[away] * self.defense[home] * aa
        return max(eh, 1e-3), max(ea, 1e-3)

    def probabilities(
        self, home: str, away: str, *, neutral: bool = False, max_goals: int = 8
    ) -> tuple[float, float, float]:
        eh, ea = self.expected_goals(home, away, neutral=neutral)
        ph = [_pmf(i, eh) for i in range(max_goals + 1)]
        pa = [_pmf(j, ea) for j in range(max_goals + 1)]
        p_home = p_draw = p_away = 0.0
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                p = ph[i] * pa[j]
                if i > j:
                    p_home += p
                elif i == j:
                    p_draw += p
                else:
                    p_away += p
        total = p_home + p_draw + p_away
        return (p_home / total, p_draw / total, p_away / total)

    def most_likely_score(
        self, home: str, away: str, *, neutral: bool = False, max_goals: int = 8
    ) -> tuple[int, int]:
        eh, ea = self.expected_goals(home, away, neutral=neutral)
        best, best_p = (0, 0), -1.0
        for i in range(max_goals + 1):
            for j in range(max_goals + 1):
                p = _pmf(i, eh) * _pmf(j, ea)
                if p > best_p:
                    best, best_p = (i, j), p
        return best


def fit_poisson(results: pd.DataFrame) -> PoissonModel:
    """Estimate attack/defense factors from a results history."""
    scored: dict[str, int] = defaultdict(int)
    conceded: dict[str, int] = defaultdict(int)
    games: dict[str, int] = defaultdict(int)

    for row in results.itertuples(index=False):
        scored[row.home] += row.home_goals
        conceded[row.home] += row.away_goals
        games[row.home] += 1
        scored[row.away] += row.away_goals
        conceded[row.away] += row.home_goals
        games[row.away] += 1

    n_matches = len(results)
    mean_home = float(results["home_goals"].mean()) if n_matches else 1.3
    mean_away = float(results["away_goals"].mean()) if n_matches else 1.1
    mu = (mean_home + mean_away) / 2.0 or 1.0

    attack = {t: (scored[t] / games[t]) / mu for t in games}
    defense = {t: (conceded[t] / games[t]) / mu for t in games}
    return PoissonModel(
        attack=attack,
        defense=defense,
        mu=mu,
        home_adj=mean_home / mu,
        away_adj=mean_away / mu,
    )


def _pmf(k: int, lam: float) -> float:
    return math.exp(-lam) * lam**k / math.factorial(k)
