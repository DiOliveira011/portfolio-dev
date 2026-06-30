"""Tests for the NF-e parser and validations."""

from __future__ import annotations

import pytest

from nfe.parser import NFeError, parse_nfe
from nfe.sample import SAMPLE_NFE_XML


def test_parse_sample_header() -> None:
    nfe = parse_nfe(SAMPLE_NFE_XML)
    assert len(nfe.chave) == 44 and nfe.chave.isdigit()
    assert nfe.numero == "7"
    assert nfe.serie == "1"
    assert "TGMOB" in nfe.emitente["nome"]
    assert nfe.destinatario["nome"].startswith("Buffet")


def test_parse_items_and_totais() -> None:
    nfe = parse_nfe(SAMPLE_NFE_XML)
    assert len(nfe.itens) == 3
    first = nfe.itens[0]
    assert first.codigo == "A100"
    assert first.valor_total == 600.0
    assert nfe.totais["produtos"] == 1500.0
    assert nfe.totais["nota"] == 1500.0


def test_sample_is_valid() -> None:
    nfe = parse_nfe(SAMPLE_NFE_XML)
    assert nfe.valido
    assert all(v["ok"] for v in nfe.validacoes)


def test_total_mismatch_flagged() -> None:
    tampered = SAMPLE_NFE_XML.replace("<vProd>1500.00</vProd>", "<vProd>9999.00</vProd>")
    nfe = parse_nfe(tampered)
    assert not nfe.valido  # soma dos itens != total declarado


def test_non_nfe_raises() -> None:
    with pytest.raises(NFeError):
        parse_nfe("<html><body>não é nota</body></html>")
