"""Rules data for D&D 5e character building (free SRD-style content)."""

from __future__ import annotations

ABILITIES = ["FOR", "DES", "CON", "INT", "SAB", "CAR"]
ABILITY_NAMES = {
    "FOR": "Força", "DES": "Destreza", "CON": "Constituição",
    "INT": "Inteligência", "SAB": "Sabedoria", "CAR": "Carisma",
}

#: Standard array (assign to taste).
STANDARD_ARRAY = [15, 14, 13, 12, 10, 8]

#: Skill → governing ability.
SKILLS: dict[str, str] = {
    "Atletismo": "FOR",
    "Acrobacia": "DES", "Furtividade": "DES", "Prestidigitação": "DES",
    "Arcanismo": "INT", "História": "INT", "Investigação": "INT",
    "Natureza": "INT", "Religião": "INT",
    "Intuição": "SAB", "Lidar com Animais": "SAB", "Medicina": "SAB",
    "Percepção": "SAB", "Sobrevivência": "SAB",
    "Enganação": "CAR", "Intimidação": "CAR", "Atuação": "CAR", "Persuasão": "CAR",
}

#: Race → ability bonuses, speed (m) and a trait blurb.
RACES: dict[str, dict] = {
    "Humano": {"bonus": dict.fromkeys(ABILITIES, 1), "speed": 9, "trait": "Versátil"},
    "Elfo": {"bonus": {"DES": 2}, "speed": 9, "trait": "Visão no escuro · Sentidos aguçados"},
    "Anão": {"bonus": {"CON": 2}, "speed": 7, "trait": "Visão no escuro · Resiliência anã"},
    "Halfling": {"bonus": {"DES": 2}, "speed": 7, "trait": "Sortudo · Corajoso"},
    "Meio-Orc": {"bonus": {"FOR": 2, "CON": 1}, "speed": 9, "trait": "Resistência implacável"},
    "Tiefling": {"bonus": {"CAR": 2, "INT": 1}, "speed": 9, "trait": "Resistência a fogo"},
    "Draconato": {"bonus": {"FOR": 2, "CAR": 1}, "speed": 9, "trait": "Arma de sopro"},
    "Gnomo": {"bonus": {"INT": 2}, "speed": 7, "trait": "Astúcia gnômica"},
}

#: Class → hit die, saving-throw proficiencies, skill list, number of skills, primary ability.
CLASSES: dict[str, dict] = {
    "Guerreiro": {"hit_die": 10, "saves": ["FOR", "CON"], "num_skills": 2, "primary": "FOR",
                  "skills": ["Acrobacia", "Atletismo", "História", "Intuição",
                             "Intimidação", "Percepção", "Sobrevivência"]},
    "Mago": {"hit_die": 6, "saves": ["INT", "SAB"], "num_skills": 2, "primary": "INT",
             "skills": ["Arcanismo", "História", "Intuição", "Investigação",
                        "Medicina", "Religião"]},
    "Ladino": {"hit_die": 8, "saves": ["DES", "INT"], "num_skills": 4, "primary": "DES",
               "skills": ["Acrobacia", "Atletismo", "Enganação", "Furtividade",
                          "Intimidação", "Investigação", "Percepção", "Persuasão",
                          "Prestidigitação"]},
    "Clérigo": {"hit_die": 8, "saves": ["SAB", "CAR"], "num_skills": 2, "primary": "SAB",
                "skills": ["História", "Intuição", "Medicina", "Persuasão", "Religião"]},
    "Bárbaro": {"hit_die": 12, "saves": ["FOR", "CON"], "num_skills": 2, "primary": "FOR",
                "skills": ["Atletismo", "Intimidação", "Lidar com Animais",
                           "Natureza", "Percepção", "Sobrevivência"]},
    "Bardo": {"hit_die": 8, "saves": ["DES", "CAR"], "num_skills": 3, "primary": "CAR",
              "skills": ["Atuação", "Enganação", "História", "Intuição",
                         "Persuasão", "Acrobacia"]},
    "Patrulheiro": {"hit_die": 10, "saves": ["FOR", "DES"], "num_skills": 3, "primary": "DES",
                    "skills": ["Lidar com Animais", "Atletismo", "Furtividade",
                               "Intuição", "Investigação", "Natureza",
                               "Percepção", "Sobrevivência"]},
    "Druida": {"hit_die": 8, "saves": ["INT", "SAB"], "num_skills": 2, "primary": "SAB",
               "skills": ["Arcanismo", "Lidar com Animais", "Intuição", "Medicina",
                          "Natureza", "Percepção", "Religião", "Sobrevivência"]},
}
