"""Tests for the TF-IDF retriever."""

from __future__ import annotations

from rag.corpus import DOCS
from rag.retriever import Retriever, tokenize

R = Retriever(DOCS)


def test_tokenize_strips_stopwords_and_accents() -> None:
    toks = tokenize("Quantos dias de férias eu tenho?")
    assert "ferias" in toks
    assert "de" not in toks and "eu" not in toks


def test_retrieves_relevant_doc() -> None:
    assert R.retrieve("quantos dias de férias eu tenho")[0]["title"] == "Política de Férias"
    assert R.retrieve("como abrir um chamado de TI")[0]["title"] == "Suporte de TI"
    assert R.retrieve("vale refeição e gympass")[0]["title"] == "Benefícios"


def test_unrelated_returns_empty() -> None:
    assert R.retrieve("xyzzy plughwff zorkmid") == []


def test_scores_descending() -> None:
    hits = R.retrieve("reembolso de despesas de viagem", k=3)
    scores = [h["score"] for h in hits]
    assert scores == sorted(scores, reverse=True)
