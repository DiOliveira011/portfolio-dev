"""Tests for the delivery domain logic."""

from __future__ import annotations

from datetime import date

from gentregas import core


def test_make_defaults() -> None:
    rec = core.make("Cliente X", "Praça 1", "Caroline", "2025-01-10", valor=100, sla_dias=2)
    assert rec["status"] == "Pendente"
    assert rec["cliente"] == "Cliente X"
    assert rec["sla_dias"] == 2
    assert rec["criado_em"]


def test_prazo_uses_business_days() -> None:
    rec = core.make("c", "l", "r", "2025-01-03", sla_dias=2)  # sexta
    assert core.prazo_date(rec) == date(2025, 1, 7)           # pula fds -> terça


def test_effective_status_atrasado_and_pendente() -> None:
    past = core.make("c", "l", "r", "2024-01-10", sla_dias=2)
    assert core.effective_status(past, today=date(2024, 1, 20)) == "Atrasado"
    future = core.make("c", "l", "r", "2099-01-01", sla_dias=2)
    assert core.effective_status(future, today=date(2024, 1, 1)) == "Pendente"


def test_baixa_and_on_time() -> None:
    rec = core.make("c", "l", "r", "2025-01-03", sla_dias=2)  # prazo 07/01
    rec["entregue_em"] = ""  # ensure clean
    core.baixa(rec, "Conferente Y", usuario="op")
    assert rec["status"] == "Entregue"
    assert rec["conferente"] == "Conferente Y"
    assert rec["entregue_em"]
    assert core.effective_status(rec) == "Entregue"


def test_is_on_time() -> None:
    rec = core.make("c", "l", "r", "2025-01-03", sla_dias=2)  # prazo 07/01
    rec["status"] = "Entregue"
    rec["entregue_em"] = "2025-01-06T10:00:00"  # antes do prazo
    assert core.is_on_time(rec) is True
    rec["entregue_em"] = "2025-01-20T10:00:00"  # depois do prazo
    assert core.is_on_time(rec) is False


def test_enrich_fields() -> None:
    rec = core.make("c", "l", "r", "2025-01-03", sla_dias=2)
    e = core.enrich(rec)
    assert e["prazo_br"] == "07/01/2025"
    assert e["data_br"] == "03/01/2025"
    assert e["status_efetivo"] in core.EFFECTIVE_STATUSES
