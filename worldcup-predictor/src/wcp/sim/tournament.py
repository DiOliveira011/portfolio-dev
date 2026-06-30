"""Tournament Monte Carlo: group stage + single-elimination knockout.

The bracket: ``n_groups`` groups of 4 (round-robin, top 2 advance), then a
single-elimination knockout. Match outcomes are sampled from a neutral-venue
probability function ``prob_fn(a, b) -> (p_a_win, p_draw, p_b_win)``.
"""

from __future__ import annotations

import random
from collections import defaultdict
from collections.abc import Callable

import pandas as pd

_Probs = tuple[float, float, float]
ProbFn = Callable[[str, str], _Probs]
_Cache = dict[tuple[str, str], _Probs]


def simulate(
    teams: list[str],
    prob_fn: ProbFn,
    *,
    n_sims: int = 2000,
    n_groups: int = 4,
    seed: int = 0,
) -> pd.DataFrame:
    """Run ``n_sims`` tournaments and return per-team stage probabilities."""
    group_size = 4
    expected = n_groups * group_size
    if len(teams) != expected:
        raise ValueError(f"São necessárias {expected} seleções (recebi {len(teams)}).")

    rng = random.Random(seed)
    cache = _build_cache(teams, prob_fn)
    groups = _snake_groups(teams, n_groups)

    advanced = defaultdict(int)
    semifinal = defaultdict(int)
    final = defaultdict(int)
    champion = defaultdict(int)

    for _ in range(n_sims):
        qualified: list[str] = []
        for group in groups:
            qualified.extend(_play_group(group, cache, rng))
        for team in qualified:
            advanced[team] += 1

        last_four = _knockout_round(_seed_bracket(qualified), cache, rng)
        for team in last_four:
            semifinal[team] += 1
        finalists = _knockout_round(last_four, cache, rng)
        for team in finalists:
            final[team] += 1
        winner = _knockout_round(finalists, cache, rng)
        champion[winner[0]] += 1

    rows = [
        {
            "team": team,
            "advance": advanced[team] / n_sims,
            "semifinal": semifinal[team] / n_sims,
            "final": final[team] / n_sims,
            "champion": champion[team] / n_sims,
        }
        for team in teams
    ]
    return pd.DataFrame(rows).sort_values("champion", ascending=False).reset_index(drop=True)


# -- Internals --------------------------------------------------------------
def _build_cache(teams: list[str], prob_fn: ProbFn) -> _Cache:
    cache: _Cache = {}
    for a in teams:
        for b in teams:
            if a != b:
                cache[(a, b)] = prob_fn(a, b)
    return cache


def _snake_groups(teams: list[str], n_groups: int) -> list[list[str]]:
    """Distribute (rating-ordered) teams across groups so strengths spread out."""
    groups: list[list[str]] = [[] for _ in range(n_groups)]
    for i, team in enumerate(teams):
        groups[i % n_groups].append(team)
    return groups


def _play_group(
    group: list[str], cache: dict, rng: random.Random
) -> list[str]:
    points = dict.fromkeys(group, 0)
    goal_diff = dict.fromkeys(group, 0)
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            a, b = group[i], group[j]
            outcome = _sample(cache[(a, b)], rng)
            if outcome == "a":
                points[a] += 3
                goal_diff[a] += 1
                goal_diff[b] -= 1
            elif outcome == "b":
                points[b] += 3
                goal_diff[b] += 1
                goal_diff[a] -= 1
            else:
                points[a] += 1
                points[b] += 1
    # Rank by points, then goal difference, then a random tiebreak.
    ranked = sorted(group, key=lambda t: (points[t], goal_diff[t], rng.random()), reverse=True)
    return ranked[:2]


def _seed_bracket(qualified: list[str]) -> list[str]:
    """Order qualifiers so group winners meet runners-up (winners are even-indexed)."""
    winners = qualified[0::2]
    runners = qualified[1::2]
    bracket: list[str] = []
    for idx, winner in enumerate(winners):
        opponent = runners[(idx + 1) % len(runners)] if runners else winner
        bracket.extend([winner, opponent])
    return bracket


def _knockout_round(teams: list[str], cache: dict, rng: random.Random) -> list[str]:
    winners: list[str] = []
    for i in range(0, len(teams), 2):
        a, b = teams[i], teams[i + 1]
        winners.append(_knockout_match(a, b, cache[(a, b)], rng))
    return winners


def _knockout_match(a: str, b: str, probs: tuple[float, float, float], rng: random.Random) -> str:
    outcome = _sample(probs, rng)
    if outcome == "a":
        return a
    if outcome == "b":
        return b
    # Draw -> penalties, weighted by relative win strength.
    p_a, _p_draw, p_b = probs
    denom = p_a + p_b
    return a if (denom <= 0 or rng.random() < p_a / denom) else b


def _sample(probs: tuple[float, float, float], rng: random.Random) -> str:
    p_a, p_draw, _p_b = probs
    r = rng.random()
    if r < p_a:
        return "a"
    if r < p_a + p_draw:
        return "draw"
    return "b"
