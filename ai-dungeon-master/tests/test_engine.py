"""Tests for the offline DM engine."""

from __future__ import annotations

import random

from dungeon.engine import classify, narrate, roll_d20
from dungeon.scenarios import SCENARIOS

_SCEN = SCENARIOS["A Masmorra do Dragão Adormecido"]
_HERO = {"inventario": ["espada longa", "tocha"]}


def test_classify() -> None:
    assert classify("ataco o goblin com a espada") == "atacar"
    assert classify("olho ao redor com cuidado") == "investigar"
    assert classify("falo com o mercador") == "conversar"
    assert classify("avanço pelo corredor") == "mover"
    assert classify("pego a poção") == "pegar"
    assert classify("fujo dali") == "fugir"
    assert classify("danço uma valsa") == "outro"


def test_roll_in_range() -> None:
    rng = random.Random(0)
    assert all(1 <= roll_d20(rng) <= 20 for _ in range(100))


def test_narrate_text() -> None:
    text = narrate("ataco o inimigo", _SCEN, random.Random(3), _HERO)
    assert text.endswith("O que você faz agora?")
    assert "rolagem" in text
