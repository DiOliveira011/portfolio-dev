"""JSON-backed store for deliveries (atomic writes)."""

from __future__ import annotations

import json
from pathlib import Path


class EntregaStore:
    """Persists delivery records to a JSON file, keyed by id."""

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._items: dict[str, dict] = self._load()

    def _load(self) -> dict[str, dict]:
        if self._path.exists():
            try:
                data = json.loads(self._path.read_text(encoding="utf-8"))
                return {rec["id"]: rec for rec in data}
            except (OSError, json.JSONDecodeError, KeyError):
                return {}
        return {}

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        tmp.write_text(
            json.dumps(list(self._items.values()), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(self._path)

    # -- API ----------------------------------------------------------------
    def all(self) -> list[dict]:
        return list(self._items.values())

    def get(self, entrega_id: str) -> dict | None:
        return self._items.get(entrega_id)

    def add(self, rec: dict) -> dict:
        self._items[rec["id"]] = rec
        self._save()
        return rec

    def update(self, entrega_id: str, fields: dict) -> dict | None:
        rec = self._items.get(entrega_id)
        if rec is None:
            return None
        rec.update(fields)
        self._save()
        return rec

    def delete(self, entrega_id: str) -> None:
        if self._items.pop(entrega_id, None) is not None:
            self._save()

    def seed_if_empty(self, records: list[dict]) -> None:
        if not self._items:
            for rec in records:
                self._items[rec["id"]] = rec
            self._save()
