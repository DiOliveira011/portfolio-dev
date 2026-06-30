"""Offline Dungeon Master — deterministic narration with d20 flavor (no LLM)."""

from __future__ import annotations

import random
import unicodedata

_CATS = {
    "atacar": ("atac", "lutar", "golpe", "espada", "bater", "mata", "flecha",
               "feiti", "soco", "chut"),
    "investigar": ("invest", "olh", "examin", "procur", "vasculh", "observ",
                   "inspecion", "revist", "analis"),
    "conversar": ("convers", "fal", "pergunt", "dialog", "negoci", "grit", "respond"),
    "mover": ("andar", "avanc", "segui", "entrar", "subir", "descer", "explor",
              "caminh", "atravess", "voltar"),
    "pegar": ("peg", "coletar", "apanhar", "guardar", "saquear", "abrir", "recolh"),
    "fugir": ("fug", "fuj", "recuar", "escapar", "correr"),
}


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def classify(action: str) -> str:
    a = _norm(action)
    for cat, triggers in _CATS.items():
        if any(t in a for t in triggers):
            return cat
    return "outro"


def roll_d20(rng: random.Random) -> int:
    return rng.randint(1, 20)


def narrate(action: str, scenario: dict, rng: random.Random, character: dict) -> str:
    cat = classify(action)
    d20 = roll_d20(rng)
    arma = character["inventario"][0] if character.get("inventario") else "suas mãos"

    if cat == "atacar":
        inimigo = rng.choice(scenario["enemies"])
        if d20 >= 11:
            corpo = (f"Você avança com {arma} e atinge {inimigo} em cheio (rolagem {d20})! "
                     "A criatura recua ferida, mas o barulho ecoa pelo lugar.")
        else:
            corpo = (f"Você ataca {inimigo}, mas erra o bote (rolagem {d20}). "
                     "Ele revida e você sente o perigo aumentar.")
    elif cat == "investigar":
        pista = rng.choice(scenario["clues"])
        corpo = f"Você examina os arredores (rolagem {d20}) e nota {pista}."
    elif cat == "conversar":
        npc = rng.choice(scenario["npcs"])
        corpo = (f"Você se dirige a {npc}. Ele(a) responde com enigmas, "
                 f"deixando no ar uma pista sobre o que há adiante (rolagem {d20}).")
    elif cat == "mover":
        area = rng.choice(scenario["areas"])
        corpo = f"Você avança e chega a {area} (rolagem {d20}). O ar muda ao seu redor."
    elif cat == "pegar":
        item = rng.choice(scenario["itens"])
        corpo = f"Você encontra e recolhe {item} (rolagem {d20}). Pode ser útil mais tarde."
    elif cat == "fugir":
        if d20 >= 10:
            corpo = f"Você corre e consegue escapar do perigo por pouco (rolagem {d20})."
        else:
            corpo = (f"Você tenta fugir, mas tropeça nas sombras (rolagem {d20}). "
                     "Algo se aproxima rápido.")
    else:
        corpo = (f"Você {action.strip().rstrip('.')}. O destino hesita (rolagem {d20}) "
                 "e a cena se desenrola de forma inesperada.")

    return corpo + " O que você faz agora?"
