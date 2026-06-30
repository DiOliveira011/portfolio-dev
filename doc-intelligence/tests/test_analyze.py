"""Tests for text analytics."""

from __future__ import annotations

from docintel.analyze import extractive_summary, keywords, sentences, stats
from docintel.sample import SAMPLE_TEXT


def test_stats() -> None:
    s = stats(SAMPLE_TEXT)
    assert s["palavras"] > 50
    assert s["frases"] >= 4
    assert s["tempo_leitura_min"] >= 1


def test_keywords_finds_topic() -> None:
    tops = [w for w, _ in keywords(SAMPLE_TEXT, 10)]
    assert "nimbus" in tops


def test_extractive_summary() -> None:
    resumo = extractive_summary(SAMPLE_TEXT, 2)
    assert resumo
    assert len(resumo) < len(SAMPLE_TEXT)
    # o resumo é composto por frases reais do texto
    todas = sentences(SAMPLE_TEXT)
    assert any(frag[:20] in resumo for frag in todas)


def test_short_text_summary_returns_all() -> None:
    txt = "Frase única e curta."
    assert extractive_summary(txt, 3) == "Frase única e curta."
