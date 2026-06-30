"""Tests for character sheet building."""

from __future__ import annotations

import pytest

from rpgforge.sheet import ability_modifier, apply_race, build_character, proficiency_bonus


def test_ability_modifier() -> None:
    assert ability_modifier(10) == 0
    assert ability_modifier(16) == 3
    assert ability_modifier(8) == -1
    assert ability_modifier(20) == 5
    assert ability_modifier(7) == -2


def test_proficiency_bonus() -> None:
    assert proficiency_bonus(1) == 2
    assert proficiency_bonus(4) == 2
    assert proficiency_bonus(5) == 3
    assert proficiency_bonus(17) == 6


def test_apply_race_bonus() -> None:
    base = {"FOR": 13, "DES": 12, "CON": 13, "INT": 10, "SAB": 10, "CAR": 8}
    final = apply_race(base, "Anão")
    assert final["CON"] == 15  # +2 anão
    assert final["FOR"] == 13


def test_build_fighter_dwarf() -> None:
    base = {"FOR": 15, "DES": 14, "CON": 13, "INT": 12, "SAB": 10, "CAR": 8}
    c = build_character(name="Borin", race="Anão", klass="Guerreiro", level=1, base_scores=base)
    assert c["scores"]["CON"] == 15
    assert c["prof"] == 2
    assert c["hp"] == 12          # d10 + CON mod(+2)
    assert c["ac"] == 12          # 10 + DES mod(+2)
    assert c["primary"] == "FOR"
    save_for = next(s for s in c["saves"] if s["ability"] == "FOR")
    assert save_for["proficient"] and save_for["value"] == 4
    assert c["proficient_skills"] == ["Acrobacia", "Atletismo"]


def test_chosen_skills_are_filtered() -> None:
    base = dict.fromkeys(("FOR", "DES", "CON", "INT", "SAB", "CAR"), 10)
    c = build_character(
        name="X", race="Humano", klass="Guerreiro", level=1, base_scores=base,
        chosen_skills=["Atletismo", "Percepção", "CartaInexistente"],
    )
    assert c["proficient_skills"] == ["Atletismo", "Percepção"]


def test_invalid_race_raises() -> None:
    with pytest.raises(ValueError):
        build_character(name="x", race="Orc Cinza", klass="Mago", level=1,
                        base_scores=dict.fromkeys(("FOR", "DES", "CON", "INT", "SAB", "CAR"), 10))
