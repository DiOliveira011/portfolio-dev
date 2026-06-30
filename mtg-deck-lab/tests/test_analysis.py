"""Tests for the deck analysis (no network — cards are faked)."""

from __future__ import annotations

from mtglab import normalize_name
from mtglab.analysis import analyze
from mtglab.decklist import DeckList


def card(name, cmc=2.0, type_line="Artifact", ci=None, oracle="",
         price="1.00", land=False, legcre=False):
    return {
        "name": name, "cmc": cmc, "mana_cost": "", "type_line": type_line,
        "colors": [], "color_identity": ci or [], "oracle_text": oracle,
        "image": None, "image_small": None, "price_usd": price, "set": "TST",
        "rarity": "common", "is_land": land, "is_legendary_creature": legcre,
        "scryfall_uri": "",
    }


def build(items):
    deck = DeckList()
    cards = {}
    for qty, name, c in items:
        deck.entries.append((qty, name))
        if c:
            cards[normalize_name(name)] = c
    return deck, cards


def test_bracket_core() -> None:
    deck, cards = build([
        (1, "Sol Ring", card("Sol Ring", 1, "Artifact", price="2.00")),
        (1, "Forest", card("Forest", 0, "Basic Land — Forest", land=True, price=None)),
        (1, "Cultivate", card("Cultivate", 3, "Sorcery",
                              oracle="Search your library for basic lands.", price="0.50")),
    ])
    a = analyze(deck, cards)
    assert a.bracket == 2
    assert a.lands == 1
    assert a.tutors == 1
    assert a.mana_curve["1"] == 1
    assert a.price_usd == 2.50


def test_bracket_upgraded_with_one_game_changer() -> None:
    deck, cards = build([
        (1, "Rhystic Study", card("Rhystic Study", 3, "Enchantment", price="30")),
        (1, "Sol Ring", card("Sol Ring", 1, "Artifact", price="2")),
    ])
    a = analyze(deck, cards)
    assert "Rhystic Study" in a.game_changers
    assert a.bracket == 3


def test_bracket_optimized_many_game_changers() -> None:
    gcs = ["Rhystic Study", "Mana Drain", "Cyclonic Rift", "Demonic Tutor"]
    items = [
        (1, g, card(g, 3, "Instant",
                    oracle="search your library" if g == "Demonic Tutor" else "", price="10"))
        for g in gcs
    ]
    deck, cards = build(items)
    a = analyze(deck, cards)
    assert len(a.game_changers) == 4
    assert a.bracket == 4


def test_commander_and_color_identity() -> None:
    deck, cards = build([
        (1, "Atraxa, Praetors' Voice",
         card("Atraxa, Praetors' Voice", 4, "Legendary Creature — Angel",
              ci=["W", "U", "B", "G"], legcre=True, price="15")),
        (1, "Sol Ring", card("Sol Ring", 1, "Artifact", price="2")),
    ])
    a = analyze(deck, cards)
    assert a.commander["name"] == "Atraxa, Praetors' Voice"
    assert a.color_identity == ["B", "G", "U", "W"]
    assert a.missing == []
