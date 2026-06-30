"""Tests for provider resolution (no network)."""

from __future__ import annotations

import pytest

from dungeon import llm


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("GROQ_API_KEY", "ANTHROPIC_API_KEY", "LLM_PROVIDER"):
        monkeypatch.delenv(var, raising=False)


def test_offline_default() -> None:
    assert llm.provider() is None
    assert not llm.available()
    assert llm.complete("s", "u") is None


def test_groq_then_claude(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "x")
    assert llm.provider() == "groq"
    monkeypatch.setenv("ANTHROPIC_API_KEY", "y")
    assert llm.provider() == "claude"          # Claude tem precedência quando ambos existem
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    assert llm.provider() == "groq"            # ...salvo se forçado
