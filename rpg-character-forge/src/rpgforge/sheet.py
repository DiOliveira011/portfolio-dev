"""Build a D&D 5e character sheet from choices and ability scores."""

from __future__ import annotations

from rpgforge.data import ABILITIES, CLASSES, RACES, SKILLS


def ability_modifier(score: int) -> int:
    return (score - 10) // 2


def proficiency_bonus(level: int) -> int:
    return 2 + (level - 1) // 4


def signed(value: int) -> str:
    return f"+{value}" if value >= 0 else str(value)


def apply_race(base_scores: dict[str, int], race: str) -> dict[str, int]:
    bonus = RACES[race]["bonus"]
    return {ab: int(base_scores.get(ab, 10)) + int(bonus.get(ab, 0)) for ab in ABILITIES}


def build_character(
    *,
    name: str,
    race: str,
    klass: str,
    level: int,
    base_scores: dict[str, int],
    chosen_skills: list[str] | None = None,
) -> dict:
    """Assemble a full character sheet (raises ValueError on bad input)."""
    if race not in RACES:
        raise ValueError(f"Raça inválida: {race}")
    if klass not in CLASSES:
        raise ValueError(f"Classe inválida: {klass}")
    level = max(1, min(int(level), 20))

    cls = CLASSES[klass]
    scores = apply_race(base_scores, race)
    mods = {ab: ability_modifier(scores[ab]) for ab in ABILITIES}
    prof = proficiency_bonus(level)
    hit_die = cls["hit_die"]

    hp = hit_die + mods["CON"]
    if level > 1:
        per_level = (hit_die // 2 + 1) + mods["CON"]
        hp += (level - 1) * per_level
    hp = max(hp, 1)

    valid = [s for s in (chosen_skills or []) if s in cls["skills"]]
    proficient = valid[: cls["num_skills"]] if valid else cls["skills"][: cls["num_skills"]]
    proficient_set = set(proficient)

    saves = [
        {"ability": ab, "value": mods[ab] + (prof if ab in cls["saves"] else 0),
         "proficient": ab in cls["saves"]}
        for ab in ABILITIES
    ]
    skills = [
        {"skill": skill, "ability": ability,
         "value": mods[ability] + (prof if skill in proficient_set else 0),
         "proficient": skill in proficient_set}
        for skill, ability in SKILLS.items()
    ]
    passive = 10 + mods["SAB"] + (prof if "Percepção" in proficient_set else 0)

    return {
        "name": name or "Aventureiro(a)",
        "race": race,
        "klass": klass,
        "level": level,
        "scores": scores,
        "mods": mods,
        "prof": prof,
        "hit_die": hit_die,
        "hp": hp,
        "ac": 10 + mods["DES"],
        "initiative": mods["DES"],
        "speed": RACES[race]["speed"],
        "trait": RACES[race]["trait"],
        "primary": cls["primary"],
        "saves": saves,
        "skills": skills,
        "proficient_skills": proficient,
        "passive_perception": passive,
    }
