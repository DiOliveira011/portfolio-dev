"""Tests for the RAG service (offline-forced, no network)."""

from __future__ import annotations

import pytest

from rag import llm
from rag.service import RagService

svc = RagService()


@pytest.fixture(autouse=True)
def _force_offline(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(llm, "provider", lambda: None)


def test_answer_has_sources() -> None:
    out = svc.ask("quantos dias de férias eu tenho?")
    assert out["sources"]
    assert out["sources"][0]["title"] == "Política de Férias"
    assert out["mode"] == "offline"


def test_blank_question() -> None:
    assert svc.ask("")["mode"] == "vazio"


def test_unrelated_question() -> None:
    out = svc.ask("qual a capital da Mongólia?")
    assert out["sources"] == []
    assert "não encontrei" in out["answer"].lower()
