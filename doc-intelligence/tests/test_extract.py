"""Tests for document extraction."""

from __future__ import annotations

from docintel.extract import extract


def test_extract_txt() -> None:
    out = extract("nota.txt", "olá mundo do teste".encode())
    assert out["kind"] == "texto"
    assert "mundo" in out["text"]
    assert out["table"] is None


def test_extract_csv() -> None:
    raw = b"nome,idade\nAna,30\nBruno,25\nCarla,28\n"
    out = extract("dados.csv", raw)
    assert out["kind"] == "csv"
    assert out["table"]["linhas"] == 3
    assert out["table"]["colunas"] == 2
    assert out["table"]["cabecalho"] == ["nome", "idade"]
    assert "Ana" in out["text"]


def test_unknown_extension_falls_back_to_text() -> None:
    out = extract("leiame", b"conteudo simples")
    assert out["kind"] == "texto"
    assert "conteudo" in out["text"]


def test_corrupt_pdf_reports_warning() -> None:
    out = extract("ruim.pdf", b"isto nao e um pdf de verdade")
    assert out["text"] == ""
    assert out["warning"]
