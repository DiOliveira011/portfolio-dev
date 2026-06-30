"""Delivery domain: records, SLA prazo and effective status.

Records are plain dicts (JSON-friendly). Derived fields (prazo, status efetivo,
no prazo) are computed on demand by :func:`enrich`.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime

from gentregas.holidays import add_business_days

STATUSES = ["Pendente", "Em rota", "Entregue"]
EFFECTIVE_STATUSES = ["Pendente", "Em rota", "Entregue", "Atrasado"]
DEFAULT_SLA = 2


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_date(value: str) -> date:
    return date.fromisoformat(value[:10])


def make(
    cliente: str,
    local: str,
    responsavel: str,
    data_agendada: str,
    *,
    valor: float = 0.0,
    sla_dias: int = DEFAULT_SLA,
    observacoes: str = "",
    usuario: str = "sistema",
) -> dict:
    """Create a new delivery record."""
    return {
        "id": uuid.uuid4().hex[:10],
        "cliente": cliente,
        "local": local,
        "responsavel": responsavel,
        "data_agendada": data_agendada,
        "valor": float(valor or 0),
        "sla_dias": int(sla_dias),
        "status": "Pendente",
        "conferente": "",
        "observacoes": observacoes,
        "entregue_em": "",
        "criado_por": usuario,
        "criado_em": _now(),
        "editado_por": "",
        "editado_em": "",
    }


def prazo_date(rec: dict) -> date:
    """SLA deadline = agendada + sla_dias business days."""
    return add_business_days(
        parse_date(rec["data_agendada"]), int(rec.get("sla_dias", DEFAULT_SLA))
    )


def effective_status(rec: dict, today: date | None = None) -> str:
    """Stored status, but 'Atrasado' when past the deadline and not delivered."""
    if rec.get("status") == "Entregue":
        return "Entregue"
    today = today or date.today()
    return "Atrasado" if today > prazo_date(rec) else rec.get("status", "Pendente")


def is_on_time(rec: dict) -> bool | None:
    """Whether a delivered record met its deadline (``None`` if not delivered)."""
    if rec.get("status") != "Entregue" or not rec.get("entregue_em"):
        return None
    try:
        return parse_date(rec["entregue_em"]) <= prazo_date(rec)
    except ValueError:
        return None


def baixa(rec: dict, conferente: str, *, usuario: str = "sistema") -> dict:
    """Mark a delivery as completed (entregue) with the receiver (conferente)."""
    rec["status"] = "Entregue"
    rec["conferente"] = conferente
    rec["entregue_em"] = _now()
    rec["editado_por"] = usuario
    rec["editado_em"] = _now()
    return rec


def enrich(rec: dict, today: date | None = None) -> dict:
    """Return ``rec`` plus display/derived fields."""
    out = dict(rec)
    deadline = prazo_date(rec)
    out["prazo"] = deadline.isoformat()
    out["prazo_br"] = deadline.strftime("%d/%m/%Y")
    out["status_efetivo"] = effective_status(rec, today)
    out["atrasado"] = out["status_efetivo"] == "Atrasado"
    out["no_prazo"] = is_on_time(rec)
    try:
        out["data_br"] = parse_date(rec["data_agendada"]).strftime("%d/%m/%Y")
    except ValueError:
        out["data_br"] = rec.get("data_agendada", "")
    return out
