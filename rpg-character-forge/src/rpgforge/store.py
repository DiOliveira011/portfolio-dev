"""Persist character *build inputs* to JSON (sheets are rebuilt on view)."""

from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path


class CharacterStore:
    """JSON-backed store of saved character build inputs."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._items: dict[str, dict] = self._load()

    def _load(self) -> dict[str, dict]:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                return {}
        return {}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self._items, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self._path)

    def save(self, inputs: dict, summary: dict) -> str:
        char_id = uuid.uuid4().hex[:10]
        self._items[char_id] = {
            "id": char_id,
            "inputs": inputs,
            "summary": summary,
            "saved_at": datetime.now(UTC).isoformat(),
        }
        self._save()
        return char_id

    def get(self, char_id: str) -> dict | None:
        return self._items.get(char_id)

    def delete(self, char_id: str) -> None:
        if self._items.pop(char_id, None) is not None:
            self._save()

    def list(self) -> list[dict]:
        return sorted(self._items.values(), key=lambda c: c.get("saved_at", ""), reverse=True)
