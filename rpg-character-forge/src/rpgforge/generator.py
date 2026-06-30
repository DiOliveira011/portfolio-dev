"""Random character generation (rolled scores + sensible assignment)."""

from __future__ import annotations

import random

from rpgforge.data import ABILITIES, CLASSES, RACES
from rpgforge.sheet import build_character

_NAMES = [
    "Thorin", "Lyra", "Aragorn", "Mira", "Kael", "Selene", "Bran", "Eldrin",
    "Naya", "Drogan", "Vex", "Orla", "Fenn", "Sariel", "Borin", "Isolde",
]
# Priority for assigning the remaining high rolls after the primary ability.
_PRIORITY = ["CON", "DES", "SAB", "CAR", "INT", "FOR"]


def roll_4d6_drop_lowest(rng: random.Random) -> int:
    rolls = sorted(rng.randint(1, 6) for _ in range(4))
    return sum(rolls[1:])


def rolled_scores(rng: random.Random) -> list[int]:
    return [roll_4d6_drop_lowest(rng) for _ in range(6)]


def random_inputs(seed: int | None = None) -> dict:
    """Return random build inputs (name/race/class/level/scores/skills)."""
    rng = random.Random(seed)
    race = rng.choice(list(RACES))
    klass = rng.choice(list(CLASSES))
    level = rng.choice([1, 1, 1, 2, 3, 4, 5])
    scores = sorted(rolled_scores(rng), reverse=True)

    primary = CLASSES[klass]["primary"]
    order = [primary] + [ab for ab in _PRIORITY if ab != primary]
    base = dict.fromkeys(ABILITIES, 10)
    for ability, value in zip(order, scores, strict=False):
        base[ability] = value

    cls_skills = CLASSES[klass]["skills"]
    chosen = rng.sample(cls_skills, min(CLASSES[klass]["num_skills"], len(cls_skills)))
    return {
        "name": rng.choice(_NAMES),
        "race": race,
        "klass": klass,
        "level": level,
        "base_scores": base,
        "chosen_skills": chosen,
    }


def random_character(seed: int | None = None) -> dict:
    """Build a full random character sheet."""
    return build_character(**random_inputs(seed))
