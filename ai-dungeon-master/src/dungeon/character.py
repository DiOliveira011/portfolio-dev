"""Lightweight hero generation for a campaign."""

from __future__ import annotations

import random

_NOMES = ["Kaelen", "Sora", "Brundir", "Mirel", "Tharok", "Lyssa", "Garrick", "Nyva",
          "Edda", "Roran", "Senna", "Dorn"]
_CLASSES = {
    "Guerreiro": {"hp": 14, "arma": "espada longa"},
    "Mago": {"hp": 8, "arma": "cajado arcano"},
    "Ladino": {"hp": 10, "arma": "adagas gêmeas"},
    "Patrulheiro": {"hp": 12, "arma": "arco curto"},
    "Clérigo": {"hp": 11, "arma": "maça sagrada"},
}


def random_character(rng: random.Random | None = None, nome: str = "") -> dict:
    rng = rng or random.Random()
    classe = rng.choice(list(_CLASSES))
    info = _CLASSES[classe]
    return {
        "nome": (nome or rng.choice(_NOMES)).strip() or "Aventureiro(a)",
        "classe": classe,
        "hp": info["hp"],
        "hp_max": info["hp"],
        "inventario": [info["arma"], "tocha", "5 moedas de ouro"],
    }
