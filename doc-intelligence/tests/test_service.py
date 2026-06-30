"""Tests for the service (offline-forced) and provider resolution."""

from __future__ import annotations

import pytest

from docintel import llm
from docintel.sample import SAMPLE_TEXT
from docintel.service import analyze_text, summarize


@pytest.fixture(autouse=True)
def _offline(monkeypatch: pytest.MonkeyPatch) -> None:
    for var in ("GROQ_API_KEY", "ANTHROPIC_API_KEY", "LLM_PROVIDER"):
        monkeypatch.delenv(var, raising=False)


def test_analyze_text_keys() -> None:
    out = analyze_text(SAMPLE_TEXT)
    assert set(out) == {"stats", "keywords", "extractive"}
    assert out["extractive"]


def test_summarize_offline() -> None:
    out = summarize(SAMPLE_TEXT)
    assert out["mode"] == "offline"
    assert out["summary"]
    assert out["bullets"]
    assert "Offline" in out["provider"]


def test_summarize_blank() -> None:
    assert summarize("")["mode"] == "vazio"


def test_provider_detection(monkeypatch: pytest.MonkeyPatch) -> None:
    assert llm.provider() is None
    monkeypatch.setenv("GROQ_API_KEY", "x")
    assert llm.provider() == "groq"
