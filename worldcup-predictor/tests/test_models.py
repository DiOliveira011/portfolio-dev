"""Tests for the Elo and Poisson models."""

from __future__ import annotations

from wcp.data import generate_sample_history
from wcp.models import compute_ratings, fit_poisson, win_draw_loss


def test_elo_ratings_rank_strong_teams_high() -> None:
    results = generate_sample_history(n_matches=1500, seed=3)
    ratings = compute_ratings(results)
    ranked = sorted(ratings, key=ratings.get, reverse=True)
    # Brasil/França/Argentina are the hidden-strongest; expect them near the top.
    assert "Brasil" in ranked[:4]
    assert ratings["Brasil"] > ratings["Coreia do Sul"]


def test_win_draw_loss_sums_to_one_and_favours_stronger() -> None:
    p_a, p_draw, p_b = win_draw_loss(1750, 1500)
    assert abs(p_a + p_draw + p_b - 1.0) < 1e-9
    assert p_a > p_b


def test_poisson_probabilities_valid() -> None:
    results = generate_sample_history(n_matches=1500, seed=3)
    model = fit_poisson(results)
    p_home, p_draw, p_away = model.probabilities("Brasil", "Japão", neutral=True)
    assert abs(p_home + p_draw + p_away - 1.0) < 1e-9
    assert p_home > p_away  # Brasil is stronger
    score = model.most_likely_score("Brasil", "Japão", neutral=True)
    assert isinstance(score[0], int) and isinstance(score[1], int)
