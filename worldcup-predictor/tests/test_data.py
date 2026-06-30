"""Tests for data generation and loading."""

from __future__ import annotations

from wcp.data import generate_sample_history, load_results, teams_in


def test_generate_sample_history() -> None:
    df = generate_sample_history(n_matches=200, seed=1)
    assert len(df) == 200
    assert {"home", "away", "home_goals", "away_goals"}.issubset(df.columns)
    assert (df["home_goals"] >= 0).all()
    assert len(teams_in(df)) == 16


def test_load_results_with_aliases() -> None:
    csv = (
        "mandante,visitante,gols_mandante,gols_visitante\n"
        "Brasil,Argentina,2,1\n"
        "França,Espanha,0,0\n"
    )
    df = load_results(csv)
    assert list(df.columns)[:4] == ["home", "away", "home_goals", "away_goals"]
    assert len(df) == 2
    assert df.iloc[0]["home_goals"] == 2
