"""Tests for the JSON store."""

from __future__ import annotations

from pathlib import Path

from gentregas import core
from gentregas.sample import sample_records
from gentregas.store import EntregaStore


def test_crud_and_persistence(tmp_path: Path) -> None:
    path = tmp_path / "entregas.json"
    store = EntregaStore(path)
    rec = core.make("Cliente", "Local", "Caroline", "2025-01-10")
    store.add(rec)

    assert store.get(rec["id"]) is not None
    store.update(rec["id"], {"status": "Em rota"})
    assert store.get(rec["id"])["status"] == "Em rota"

    # Reload from disk → persisted.
    reloaded = EntregaStore(path)
    assert reloaded.get(rec["id"])["status"] == "Em rota"

    store.delete(rec["id"])
    assert store.get(rec["id"]) is None


def test_seed_only_when_empty(tmp_path: Path) -> None:
    store = EntregaStore(tmp_path / "e.json")
    store.seed_if_empty(sample_records())
    n = len(store.all())
    assert n > 0
    store.seed_if_empty(sample_records())  # não duplica
    assert len(store.all()) == n
