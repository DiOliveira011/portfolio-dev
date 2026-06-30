"""Commander deck analysis: bracket estimate, mana curve, types and prices."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mtglab import normalize_name
from mtglab.decklist import DeckList
from mtglab.gamechangers import GAME_CHANGERS_NORM, MASS_LAND_DENIAL_NORM

# Default USD→BRL rate for the estimated price (overridable in the UI/config).
DEFAULT_USD_BRL = 5.50

_TYPE_PRIORITY = [
    "Creature", "Planeswalker", "Instant", "Sorcery", "Battle",
    "Artifact", "Enchantment", "Land",
]
_CURVE_BUCKETS = ["0", "1", "2", "3", "4", "5", "6", "7+"]

_BRACKET_NAMES = {
    1: "Exhibition", 2: "Core", 3: "Upgraded", 4: "Optimized", 5: "cEDH",
}


@dataclass(slots=True)
class CardRow:
    qty: int
    name: str
    card: dict[str, Any] | None


@dataclass(slots=True)
class Analysis:
    commander: dict[str, Any] | None
    color_identity: list[str]
    total: int
    unique: int
    lands: int
    avg_cmc: float
    mana_curve: dict[str, int]
    type_counts: dict[str, int]
    game_changers: list[str]
    mass_land_denial: list[str]
    tutors: int
    extra_turns: int
    bracket: int
    bracket_name: str
    bracket_reasons: list[str]
    price_usd: float
    price_brl: float
    rows: list[CardRow] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)


def _primary_type(type_line: str) -> str:
    for kind in _TYPE_PRIORITY:
        if kind in type_line:
            return kind
    return "Outro"


def _curve_bucket(cmc: float) -> str:
    value = int(cmc)
    return "7+" if value >= 7 else str(value)


def analyze(
    deck: DeckList,
    cards: dict[str, dict[str, Any]],
    *,
    missing: list[str] | None = None,
    usd_brl: float = DEFAULT_USD_BRL,
) -> Analysis:
    """Build a full :class:`Analysis` from a decklist and resolved card data."""
    rows: list[CardRow] = []
    curve = dict.fromkeys(_CURVE_BUCKETS, 0)
    types: dict[str, int] = {}
    color_identity: set[str] = set()
    game_changers: list[str] = []
    mass_land_denial: list[str] = []
    tutors = extra_turns = lands = 0
    cmc_sum = cmc_count = 0
    price_usd = 0.0

    for qty, name in deck.entries:
        card = cards.get(normalize_name(name))
        rows.append(CardRow(qty=qty, name=name, card=card))
        if not card:
            continue
        color_identity.update(card["color_identity"])
        norm = normalize_name(card["name"])
        if norm in GAME_CHANGERS_NORM:
            game_changers.append(card["name"])
        if norm in MASS_LAND_DENIAL_NORM:
            mass_land_denial.append(card["name"])
        oracle = (card.get("oracle_text") or "").lower()
        if "search your library" in oracle:
            tutors += qty
        if "extra turn" in oracle:
            extra_turns += qty
        if card["is_land"]:
            lands += qty
        else:
            curve[_curve_bucket(card["cmc"])] += qty
            cmc_sum += card["cmc"] * qty
            cmc_count += qty
        types[_primary_type(card["type_line"])] = (
            types.get(_primary_type(card["type_line"]), 0) + qty
        )
        if card.get("price_usd"):
            price_usd += float(card["price_usd"]) * qty

    commander = _resolve_commander(deck, cards)
    bracket, reasons = _estimate_bracket(
        len(game_changers), len(mass_land_denial), tutors, extra_turns
    )

    return Analysis(
        commander=commander,
        color_identity=sorted(color_identity),
        total=deck.total,
        unique=deck.unique,
        lands=lands,
        avg_cmc=(cmc_sum / cmc_count) if cmc_count else 0.0,
        mana_curve=curve,
        type_counts=dict(sorted(types.items(), key=lambda kv: kv[1], reverse=True)),
        game_changers=sorted(set(game_changers)),
        mass_land_denial=sorted(set(mass_land_denial)),
        tutors=tutors,
        extra_turns=extra_turns,
        bracket=bracket,
        bracket_name=_BRACKET_NAMES[bracket],
        bracket_reasons=reasons,
        price_usd=round(price_usd, 2),
        price_brl=round(price_usd * usd_brl, 2),
        rows=rows,
        missing=missing or [],
    )


def _resolve_commander(
    deck: DeckList, cards: dict[str, dict[str, Any]]
) -> dict[str, Any] | None:
    if deck.commander:
        card = cards.get(normalize_name(deck.commander))
        if card:
            return card
    # Guess: first legendary creature in the list.
    for _, name in deck.entries:
        card = cards.get(normalize_name(name))
        if card and card["is_legendary_creature"]:
            return card
    return None


def _estimate_bracket(
    gc: int, mld: int, tutors: int, extra_turns: int
) -> tuple[int, list[str]]:
    """Heuristic bracket estimate with human-readable reasons."""
    reasons = [
        f"{gc} Game Changer(s)",
        f"{mld} carta(s) de mass land denial",
        f"{tutors} tutor(es)",
        f"{extra_turns} carta(s) de turno extra",
    ]
    if gc == 0 and mld == 0 and tutors <= 1 and extra_turns == 0:
        reasons.append("Sem Game Changers/combos pesados → nível de precon.")
        return 2, reasons
    if gc <= 3 and mld == 0:
        reasons.append("Poucos Game Changers, sem land denial → deck ajustado.")
        return 3, reasons
    reasons.append("Muitos Game Changers / land denial → alto poder.")
    reasons.append("Bracket 5 (cEDH) é auto-declarado — confirme se for o caso.")
    return 4, reasons
