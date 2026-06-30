"""Tests for the tournament Monte Carlo simulation."""

from __future__ import annotations

from wcp.data import generate_sample_history, teams_in
from wcp.predict import build_elo
from wcp.sim import simulate


def test_simulation_probabilities_are_consistent() -> None:
    results = generate_sample_history(n_matches=1500, seed=3)
    teams = teams_in(results)
    _ratings, prob = build_elo(results)
    table = simulate(teams, prob, n_sims=600, seed=7)

    assert len(table) == 16
    # Exactly one champion per sim → champion probabilities sum to 1.
    assert round(table["champion"].sum(), 6) == 1.0
    # 8 teams advance per sim → advance probabilities sum to 8.
    assert round(table["advance"].sum(), 6) == 8.0
    # Every probability is in [0, 1].
    for col in ("advance", "semifinal", "final", "champion"):
        assert table[col].between(0.0, 1.0).all()


def test_strong_team_more_likely_champion_than_weak() -> None:
    results = generate_sample_history(n_matches=1500, seed=3)
    teams = teams_in(results)
    _ratings, prob = build_elo(results)
    table = simulate(teams, prob, n_sims=1500, seed=7).set_index("team")
    assert table.loc["Brasil", "champion"] > table.loc["Coreia do Sul", "champion"]


def test_simulate_rejects_wrong_team_count() -> None:
    import pytest

    _ratings, prob = build_elo(generate_sample_history(n_matches=300, seed=1))
    with pytest.raises(ValueError):
        simulate(["A", "B", "C"], prob, n_sims=10)
