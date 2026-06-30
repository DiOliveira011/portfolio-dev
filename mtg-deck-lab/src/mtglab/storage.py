"""Persist registered decks to a local JSON file."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class DeckStore:
    """A tiny JSON-backed store for saved decks."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._decks: dict[str, dict[str, Any]] = self._load()

    def _load(self) -> dict[str, dict[str, Any]]:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return {}
        return {}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(
            json.dumps(self._decks, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def save(self, name: str, decklist_text: str, summary: dict[str, Any]) -> str:
        """Store a deck and return its id."""
        deck_id = uuid.uuid4().hex[:10]
        self._decks[deck_id] = {
            "id": deck_id,
            "name": name or "Deck sem nome",
            "decklist": decklist_text,
            "summary": summary,
            "saved_at": datetime.now(UTC).isoformat(),
        }
        self._save()
        return deck_id

    def get(self, deck_id: str) -> dict[str, Any] | None:
        return self._decks.get(deck_id)

    def delete(self, deck_id: str) -> None:
        if deck_id in self._decks:
            del self._decks[deck_id]
            self._save()

    def list(self) -> list[dict[str, Any]]:
        """Saved decks, newest first (without the full decklist text)."""
        items = sorted(
            self._decks.values(), key=lambda d: d.get("saved_at", ""), reverse=True
        )
        return [{k: v for k, v in d.items() if k != "decklist"} for d in items]
