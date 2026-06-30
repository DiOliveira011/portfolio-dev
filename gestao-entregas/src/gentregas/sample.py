"""Seed data so the app opens already populated (a real operation day)."""

from __future__ import annotations

from datetime import date, timedelta

from gentregas.core import make

RESPONSAVEIS = ["Caroline", "Yasmin", "Marcos"]

# (cliente, local, responsável, dias_offset, valor, status, entregue_offset, conferente)
_RAW = [
    ("Buffet Jardins", "Pinheiros", "Caroline", -6, 12000, "Entregue", -5, "João Silva"),
    ("Hotel Paulista", "Bela Vista", "Yasmin", -4, 8200, "Entregue", -1, "Marina Alves"),
    ("Espaço Vila Mariana", "Vila Mariana", "Caroline", -3, 15400, "Em rota", None, ""),
    ("Centro de Eventos Norte", "Santana", "Marcos", -2, 9800, "Pendente", None, ""),
    ("Chácara Cotia", "Cotia", "Yasmin", -1, 21000, "Pendente", None, ""),
    ("Casa Tatuapé", "Tatuapé", "Caroline", 0, 7300, "Em rota", None, ""),
    ("Buffet Santana", "Santana", "Marcos", 0, 6400, "Pendente", None, ""),
    ("Salão Moema", "Moema", "Yasmin", 1, 11200, "Pendente", None, ""),
    ("Espaço Lapa", "Lapa", "Caroline", 1, 5400, "Pendente", None, ""),
    ("Buffet ABC", "Santo André", "Marcos", 2, 18900, "Pendente", None, ""),
    ("Casa Perdizes", "Perdizes", "Yasmin", 3, 6800, "Pendente", None, ""),
    ("Hotel Faria Lima", "Itaim", "Caroline", 4, 24500, "Pendente", None, ""),
    ("Salão Morumbi", "Morumbi", "Marcos", -8, 9100, "Entregue", -6, "Pedro Costa"),
    ("Espaço Ipiranga", "Ipiranga", "Yasmin", -5, 13300, "Pendente", None, ""),
]


def sample_records() -> list[dict]:
    """Build the seed deliveries (relative to today)."""
    today = date.today()
    records: list[dict] = []
    for cliente, local, resp, offset, valor, status, ent_off, conf in _RAW:
        rec = make(
            cliente, local, resp,
            (today + timedelta(days=offset)).isoformat(),
            valor=valor, sla_dias=2, usuario="seed",
        )
        if status == "Entregue":
            rec["status"] = "Entregue"
            rec["conferente"] = conf
            rec["entregue_em"] = (today + timedelta(days=ent_off or 0)).isoformat() + "T10:00:00"
        elif status == "Em rota":
            rec["status"] = "Em rota"
        records.append(rec)
    return records
