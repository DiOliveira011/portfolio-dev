"""Tests for random character generation."""

from __future__ import annotations

import random

from rpgforge.data import ABILITIES, CLASSES, RACES
from rpgforge.generator import random_character, random_inputs, roll_4d6_drop_lowest


def test_roll_in_range() -> None:
    rng = random.Random(0)
    for _ in range(200):
        assert 3 <= roll_4d6_drop_lowest(rng) <= 18


def test_random_inputs_valid() -> None:
    inp = random_inputs(seed=42)
    assert inp["race"] in RACES
    assert inp["klass"] in CLASSES
    assert 1 <= inp["level"] <= 20
    assert set(inp["base_scores"]) == set(ABILITIES)
    assert all(3 <= v <= 18 for v in inp["base_scores"].values())


def test_random_character_builds() -> None:
    c = random_character(seed=7)
    assert c["hp"] > 0
    assert c["name"]
    assert c["scores"][c["primary"]] >= 8


def test_determinism() -> None:
    a = random_inputs(seed=5)
    b = random_inputs(seed=5)
    assert a == b
