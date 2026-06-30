"""Historical match data: loading real CSVs and generating a synthetic history.

Canonical schema (DataFrame): ``home``, ``away`` (str), ``home_goals``,
``away_goals`` (int), optional ``date``.
"""

from __future__ import annotations

import io
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

#: Hidden "true" attacking strength per team — only used to *generate* a
#: plausible history. The models must recover strengths from the data alone.
_TRUE_STRENGTH: dict[str, float] = {
    "Brasil": 1.90, "França": 1.85, "Argentina": 1.82, "Espanha": 1.65,
    "Inglaterra": 1.62, "Alemanha": 1.58, "Portugal": 1.52, "Holanda": 1.48,
    "Bélgica": 1.42, "Itália": 1.35, "Croácia": 1.30, "Uruguai": 1.25,
    "Marrocos": 1.18, "México": 1.05, "Japão": 1.02, "Coreia do Sul": 0.95,
}
DEFAULT_TEAMS: list[str] = list(_TRUE_STRENGTH)

_BASE_GOALS = 1.30
_HOME_ADV = 0.30

_COLUMN_ALIASES = {
    "home": {"home", "mandante", "home_team", "team_home", "casa"},
    "away": {"away", "visitante", "away_team", "team_away", "fora"},
    "home_goals": {"home_goals", "home_score", "gols_mandante", "placar_casa", "hg"},
    "away_goals": {"away_goals", "away_score", "gols_visitante", "placar_fora", "ag"},
}


def _expected_goals(strength_for: float, strength_against: float, *, home: bool) -> float:
    edge = 0.5 * (strength_for - strength_against) + (_HOME_ADV if home else 0.0)
    return _BASE_GOALS * float(np.exp(edge))


def generate_sample_history(*, n_matches: int = 600, seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic but realistic match history among the default teams."""
    rng = np.random.default_rng(seed)
    teams = DEFAULT_TEAMS
    start = date.today() - timedelta(days=8 * 365)
    rows: list[dict[str, object]] = []
    for i in range(n_matches):
        home, away = rng.choice(teams, size=2, replace=False)
        lam_home = _expected_goals(_TRUE_STRENGTH[home], _TRUE_STRENGTH[away], home=True)
        lam_away = _expected_goals(_TRUE_STRENGTH[away], _TRUE_STRENGTH[home], home=False)
        rows.append(
            {
                "date": start + timedelta(days=int(i * 4)),
                "home": home,
                "away": away,
                "home_goals": int(rng.poisson(lam_home)),
                "away_goals": int(rng.poisson(lam_away)),
            }
        )
    return pd.DataFrame(rows)


def load_results(source: object) -> pd.DataFrame:
    """Load a results CSV (path/bytes/str/buffer) into the canonical schema."""
    if (isinstance(source, (str, Path)) and Path(source).exists()) or hasattr(source, "read"):
        raw = pd.read_csv(source)
    elif isinstance(source, bytes):
        raw = pd.read_csv(io.BytesIO(source))
    elif isinstance(source, str):
        raw = pd.read_csv(io.StringIO(source))
    else:
        raise TypeError(f"Unsupported source: {type(source)!r}")

    rename: dict[str, str] = {}
    for col in raw.columns:
        key = str(col).strip().lower()
        for canonical, aliases in _COLUMN_ALIASES.items():
            if key in aliases:
                rename[col] = canonical
    raw = raw.rename(columns=rename)

    required = {"home", "away", "home_goals", "away_goals"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"CSV sem as colunas necessárias: {', '.join(sorted(missing))}")

    raw["home_goals"] = pd.to_numeric(raw["home_goals"], errors="coerce")
    raw["away_goals"] = pd.to_numeric(raw["away_goals"], errors="coerce")
    raw = raw.dropna(subset=["home", "away", "home_goals", "away_goals"])
    raw["home_goals"] = raw["home_goals"].astype(int)
    raw["away_goals"] = raw["away_goals"].astype(int)
    return raw.reset_index(drop=True)


def teams_in(results: pd.DataFrame) -> list[str]:
    """Sorted list of distinct teams appearing in the results."""
    return sorted(set(results["home"]) | set(results["away"]))
