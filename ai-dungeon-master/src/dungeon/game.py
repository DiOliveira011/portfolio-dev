"""Game master: runs a campaign, using the LLM when available, engine otherwise."""

from __future__ import annotations

import random
import uuid
from dataclasses import dataclass, field

from dungeon import engine, llm
from dungeon.character import random_character
from dungeon.scenarios import SCENARIOS

_DM_SYSTEM = (
    "Você é um Mestre de RPG (Dungeon Master) narrando uma aventura de fantasia "
    "sombria em português do Brasil. Seja vívido e conciso (2 a 4 frases), mantenha "
    "a continuidade com o histórico, respeite as ações do jogador e SEMPRE termine "
    "com uma deixa ou pergunta para o jogador decidir o próximo passo. Não decida "
    "pelo jogador."
)


@dataclass
class Campaign:
    id: str
    scenario: str
    character: dict
    log: list[dict] = field(default_factory=list)   # {"who": "dm"|"jogador", "text": str}
    turn: int = 0


def new_campaign(scenario: str, hero_name: str = "", seed: int | None = None) -> Campaign:
    if scenario not in SCENARIOS:
        scenario = next(iter(SCENARIOS))
    rng = random.Random(seed)
    char = random_character(rng, hero_name)
    abertura = (
        f"{SCENARIOS[scenario]['intro']}\n\n"
        f"Você é {char['nome']}, {char['classe']} (PV {char['hp']}). "
        f"Empunha {char['inventario'][0]}. O que você faz?"
    )
    return Campaign(id=uuid.uuid4().hex[:10], scenario=scenario, character=char,
                    log=[{"who": "dm", "text": abertura}])


def _memory(camp: Campaign) -> str:
    recent = camp.log[-8:]
    hist = "\n".join(
        f"{'Mestre' if e['who'] == 'dm' else 'Jogador'}: {e['text']}" for e in recent
    )
    c = camp.character
    return (
        f"Cenário: {camp.scenario}\n"
        f"Herói: {c['nome']}, {c['classe']} (PV {c['hp']}/{c['hp_max']})\n"
        f"Inventário: {', '.join(c['inventario'])}\n\n"
        f"Histórico recente:\n{hist}"
    )


def _llm_narrate(camp: Campaign, action: str) -> str | None:
    user = f"{_memory(camp)}\n\nAção do jogador: {action}"
    return llm.complete(_DM_SYSTEM, user, max_tokens=320, temperature=0.85)


def act(camp: Campaign, action: str, *, seed: int | None = None) -> None:
    action = (action or "").strip()
    if not action:
        return
    camp.log.append({"who": "jogador", "text": action})
    camp.turn += 1
    text = _llm_narrate(camp, action) if llm.available() else None
    if not text:
        text = engine.narrate(action, SCENARIOS[camp.scenario], random.Random(seed),
                              camp.character)
    camp.log.append({"who": "dm", "text": text})
