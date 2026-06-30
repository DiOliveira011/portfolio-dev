"""Curated lists used by the Commander **bracket** heuristic.

``GAME_CHANGERS`` is a representative subset of WotC's official "Game Changers"
list (the cards that push a deck toward higher brackets). It is versioned here so
the analysis runs offline; expand it as the official list evolves.
"""

from __future__ import annotations

from mtglab import normalize_name

# Representative subset of the official Game Changers list.
GAME_CHANGERS: list[str] = [
    # Fast mana / rocks
    "Ancient Tomb", "Chrome Mox", "Mox Diamond", "Jeweled Lotus", "Mana Vault",
    "Grim Monolith", "Lion's Eye Diamond", "The One Ring", "Gaea's Cradle",
    "Serra's Sanctum",
    # Tutors
    "Demonic Tutor", "Vampiric Tutor", "Imperial Seal", "Grim Tutor",
    "Enlightened Tutor", "Mystical Tutor", "Personal Tutor", "Tainted Pact",
    # Card advantage / stax / hatebears
    "Rhystic Study", "Mystic Remora", "Smothering Tithe", "Necropotence",
    "Esper Sentinel", "Opposition Agent", "Drannith Magistrate", "Notion Thief",
    "Grand Arbiter Augustin IV", "Trinisphere", "Stasis",
    # Counters / protection
    "Mana Drain", "Force of Will", "Fierce Guardianship", "Deflecting Swat",
    # Win conditions / bombs
    "Thassa's Oracle", "Underworld Breach", "Ad Nauseam", "Expropriate",
    "Cyclonic Rift", "Craterhoof Behemoth", "Bolas's Citadel",
    # Powerful commanders
    "Winota, Joiner of Forces", "Yuriko, the Tiger's Shadow", "Kinnan, Bonder Prodigy",
    "Najeela, the Blade-Blossom", "Tergrid, God of Fright", "Vorinclex, Voice of Hunger",
    # Lands
    "Glacial Chasm",
]

# Mass land denial — tracked separately (restricted in lower brackets).
MASS_LAND_DENIAL: list[str] = [
    "Armageddon", "Ravages of War", "Catastrophe", "Jokulhaups", "Obliterate",
    "Decree of Annihilation", "Devastating Dreams", "Cataclysm", "Boom // Bust",
]

GAME_CHANGERS_NORM: frozenset[str] = frozenset(normalize_name(n) for n in GAME_CHANGERS)
MASS_LAND_DENIAL_NORM: frozenset[str] = frozenset(normalize_name(n) for n in MASS_LAND_DENIAL)
