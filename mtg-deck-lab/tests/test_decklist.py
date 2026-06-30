"""Tests for decklist parsing."""

from __future__ import annotations

from mtglab.decklist import parse_decklist


def test_basic_formats() -> None:
    text = """
    1 Sol Ring
    1x Lightning Bolt
    2 Forest
    1 Arcane Signet (C21) 263
    """
    deck = parse_decklist(text)
    names = [n for _, n in deck.entries]
    assert "Sol Ring" in names
    assert "Lightning Bolt" in names
    assert "Arcane Signet" in names  # set/collector stripped
    assert deck.total == 5  # 1+1+2+1


def test_commander_tag_and_header() -> None:
    text = """
    Commander
    1 Atraxa, Praetors' Voice
    Deck
    1 Sol Ring
    """
    deck = parse_decklist(text)
    assert deck.commander == "Atraxa, Praetors' Voice"

    text2 = "1 Yuriko, the Tiger's Shadow *CMDR*\n1 Sol Ring\n"
    deck2 = parse_decklist(text2)
    assert deck2.commander == "Yuriko, the Tiger's Shadow"


def test_sideboard_is_ignored() -> None:
    text = "1 Sol Ring\nSideboard\n1 Pyroblast\n"
    deck = parse_decklist(text)
    names = [n for _, n in deck.entries]
    assert "Sol Ring" in names
    assert "Pyroblast" not in names


def test_names_includes_commander() -> None:
    deck = parse_decklist("1 Sol Ring\n1 Atraxa, Praetors' Voice *CMDR*\n")
    assert "Atraxa, Praetors' Voice" in deck.names()
