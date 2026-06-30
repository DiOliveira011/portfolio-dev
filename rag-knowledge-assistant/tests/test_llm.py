"""Tests for the provider resolution (no network calls)."""

from __future__ import annotations

import pytest

from rag import llm


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("GROQ_API_KEY", "ANTHROPIC_API_KEY", "LLM_PROVIDER"):
        monkeypatch.delenv(var, raising=False)


def test_offline_by_default() -> None:
    assert llm.provider() is None
    assert llm.available() is False
    assert "Offline" in llm.provider_label()
    assert llm.complete("s", "u") is None      # sem chave: não chama rede


def test_groq_detected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "x")
    assert llm.provider() == "groq"
    assert "Groq" in llm.provider_label()


def test_claude_detected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "x")
    assert llm.provider() == "claude"


def test_force_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "x")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "y")
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    assert llm.provider() == "groq"
