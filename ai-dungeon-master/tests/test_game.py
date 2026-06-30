"""Tests for the game master (offline-forced)."""

from __future__ import annotations

import pytest

from dungeon import llm
from dungeon.game import Campaign, act, new_campaign
from dungeon.scenarios import scenario_names


@pytest.fixture(autouse=True)
def _force_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(llm, "provider", lambda: None)


def test_scenarios_have_three() -> None:
    names = scenario_names()
    assert len(names) == 3


def test_new_campaign() -> None:
    camp = new_campaign("A Masmorra do Dragão Adormecido", hero_name="Aria", seed=1)
    assert isinstance(camp, Campaign)
    assert camp.character["nome"] == "Aria"
    assert camp.character["hp"] > 0
    assert len(camp.log) == 1 and camp.log[0]["who"] == "dm"


def test_invalid_scenario_falls_back() -> None:
    camp = new_campaign("Cenário Inexistente", seed=1)
    assert camp.scenario in scenario_names()


def test_act_appends_turns() -> None:
    camp = new_campaign("A Taverna Amaldiçoada", seed=2)
    act(camp, "investigo o salão", seed=5)
    assert camp.turn == 1
    assert len(camp.log) == 3                 # abertura + jogador + mestre
    assert camp.log[-2]["who"] == "jogador"
    assert camp.log[-1]["who"] == "dm"
    assert camp.log[-1]["text"]


def test_blank_action_ignored() -> None:
    camp = new_campaign("A Floresta dos Sussurros", seed=2)
    act(camp, "   ")
    assert camp.turn == 0 and len(camp.log) == 1
