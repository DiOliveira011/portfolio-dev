"""Parse pasted decklists in the common community formats.

Accepts MTGA/MTGO/Moxfield/Archidekt style lines such as::

    1 Sol Ring
    1x Lightning Bolt
    1 Arcane Signet (C21) 263
    1 Atraxa, Praetors' Voice *CMDR*

Commander sections ("Commander" / "Comandante" headers, or the ``*CMDR*`` tag)
are recognised. Sideboard lines (``SB:`` / "Sideboard") are ignored.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

_LINE = re.compile(r"^\s*(?:(\d+)\s*[xX]?\s+)?(.+?)\s*$")
_SET_PAREN = re.compile(r"\s*\((?:[^)]*)\)\s*\d*\s*$")   # trailing "(SET) 123"
_SET_BRACKET = re.compile(r"\s*\[[^\]]*\]\s*$")
_CMDR_TAG = re.compile(r"\*?\bCMDR\b\*?|\*Commander\*", re.IGNORECASE)
_COMMANDER_HEADER = re.compile(r"^\s*(commander|comandante)\b", re.IGNORECASE)
_SIDEBOARD = re.compile(r"^\s*(sb:|sideboard)\b", re.IGNORECASE)


@dataclass(slots=True)
class DeckList:
    """A parsed decklist: quantity/name entries plus an optional commander."""

    entries: list[tuple[int, str]] = field(default_factory=list)
    commander: str | None = None

    @property
    def total(self) -> int:
        return sum(qty for qty, _ in self.entries)

    @property
    def unique(self) -> int:
        return len(self.entries)

    def names(self) -> list[str]:
        names = [name for _, name in self.entries]
        if self.commander and self.commander not in names:
            names.append(self.commander)
        return names


def _clean_name(raw: str) -> str:
    name = _CMDR_TAG.sub("", raw)
    name = _SET_PAREN.sub("", name)
    name = _SET_BRACKET.sub("", name)
    return name.strip(" -\t")


def parse_decklist(text: str) -> DeckList:
    """Parse ``text`` into a :class:`DeckList`."""
    deck = DeckList()
    in_commander_section = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if _SIDEBOARD.match(line):
            break  # everything after a sideboard marker is ignored
        if _COMMANDER_HEADER.match(line) and not _LINE.match(line).group(1):
            in_commander_section = True
            continue
        if line.startswith("//"):
            in_commander_section = "commander" in line.lower()
            continue

        is_commander = bool(_CMDR_TAG.search(line)) or in_commander_section
        match = _LINE.match(line)
        if not match:
            continue
        qty = int(match.group(1)) if match.group(1) else 1
        name = _clean_name(match.group(2))
        if not name:
            continue
        if is_commander and deck.commander is None:
            deck.commander = name
            in_commander_section = False
        deck.entries.append((qty, name))
    return deck
