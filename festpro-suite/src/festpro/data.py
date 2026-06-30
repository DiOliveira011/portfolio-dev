"""Synthetic, deterministic dataset for the fictional company **FestPro**.

Generates a coherent operation (events/quotes, clients, inventory) that powers
every dashboard page. No file import needed — the "company" lives here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import numpy as np
import pandas as pd

REGIONS = ["Zona Sul", "Zona Norte", "Zona Leste", "Zona Oeste", "Centro", "ABC"]
EVENT_TYPES = ["Casamento", "Corporativo", "Aniversário", "Formatura", "Outro"]
SEGMENTS = ["PF", "PJ"]
VEHICLES = ["Caminhão 1", "Caminhão 2", "Van", "Caminhão 3"]
DRIVERS = ["Carlos Souza", "João Pereira", "Marcos Lima", "André Dias"]
STATUSES = ["Orçamento", "Confirmado", "Realizado", "Cancelado"]

_TYPE_MULT = {"Casamento": 1.40, "Corporativo": 1.25, "Aniversário": 1.0,
              "Formatura": 1.15, "Outro": 0.9}
_GUEST_RANGE = {"Casamento": (80, 300), "Corporativo": (50, 500),
                "Aniversário": (30, 150), "Formatura": (100, 400), "Outro": (20, 120)}

_ITEM_CATALOG = [
    ("Mesas redondas", "Mobiliário", 400), ("Cadeiras Tiffany", "Mobiliário", 2000),
    ("Cadeiras comuns", "Mobiliário", 1500), ("Sofás", "Mobiliário", 120),
    ("Pufes", "Mobiliário", 300), ("Tendas 5x5", "Estrutura", 60),
    ("Tendas 10x10", "Estrutura", 25), ("Pista de dança", "Estrutura", 30),
    ("Jogos de louça", "Louça", 800), ("Taças", "Louça", 5000),
    ("Talheres", "Louça", 6000), ("Toalhas de mesa", "Têxtil", 1200),
    ("Iluminação", "AV", 200), ("Som", "AV", 80),
    ("Buffet térmico", "Cozinha", 150), ("Climatizadores", "Conforto", 90),
]

_PF_FIRST = ["Ana", "Bruno", "Carla", "Daniel", "Eduarda", "Felipe", "Gabriela",
             "Henrique", "Isabela", "João", "Larissa", "Marcos", "Natália", "Paulo",
             "Rafaela", "Thiago", "Vanessa", "Rodrigo"]
_PF_LAST = ["Silva", "Souza", "Oliveira", "Santos", "Pereira", "Lima", "Costa",
            "Almeida", "Ribeiro", "Carvalho", "Gomes", "Martins"]
_PJ_PREFIX = ["Grupo", "Tech", "Inova", "Prime", "Global", "Nova", "Alpha", "Vértice"]
_PJ_SUFFIX = ["Corp", "Solutions", "Brasil", "Ltda", "Eventos", "Holding", "Partners"]


@dataclass(slots=True)
class CompanyData:
    """Bundle of the fictional company's tables."""

    events: pd.DataFrame
    inventory: pd.DataFrame
    clients: pd.DataFrame
    as_of: pd.Timestamp


def _client_name(rng: np.random.Generator, segment: str) -> str:
    if segment == "PJ":
        return f"{rng.choice(_PJ_PREFIX)} {rng.choice(_PJ_SUFFIX)}"
    return f"{rng.choice(_PF_FIRST)} {rng.choice(_PF_LAST)}"


def _build_clients(rng: np.random.Generator, n: int) -> pd.DataFrame:
    rows = []
    for i in range(n):
        segment = "PJ" if rng.random() < 0.4 else "PF"
        rows.append({
            "client_id": f"C{i + 1:04d}",
            "client": _client_name(rng, segment),
            "segment": segment,
            "region": rng.choice(REGIONS),
        })
    return pd.DataFrame(rows)


def _status_for(day: date, today: date, rng: np.random.Generator) -> str:
    if day > today:
        return "Orçamento" if rng.random() < 0.5 else "Confirmado"
    roll = rng.random()
    if roll < 0.80:
        return "Realizado"
    if roll < 0.92:
        return "Cancelado"
    return "Orçamento"  # quote that was never closed


def generate_company_data(
    *, seed: int = 7, n_events: int = 950, n_clients: int = 150
) -> CompanyData:
    """Generate the full company dataset (deterministic for a given seed)."""
    rng = np.random.default_rng(seed)
    today = date.today()
    clients = _build_clients(rng, n_clients)
    client_pick = rng.choice(len(clients), size=n_events, p=_recurrence_weights(rng, n_clients))

    start = today - timedelta(days=365)
    rows = []
    for k in range(n_events):
        client = clients.iloc[int(client_pick[k])]
        day = start + timedelta(days=int(rng.integers(0, 410)))  # ~13 months incl. future
        etype = str(rng.choice(EVENT_TYPES, p=[0.34, 0.26, 0.22, 0.10, 0.08]))
        lo, hi = _GUEST_RANGE[etype]
        guests = int(rng.integers(lo, hi))
        revenue = round(guests * float(rng.uniform(90, 170)) * _TYPE_MULT[etype], 2)
        cost = round(revenue * float(rng.uniform(0.55, 0.72)), 2)
        status = _status_for(day, today, rng)
        realized = status == "Realizado"
        rows.append({
            "event_id": f"E{k + 1:05d}",
            "date": pd.Timestamp(day),
            "client_id": client["client_id"],
            "client": client["client"],
            "segment": client["segment"],
            "region": client["region"],
            "type": etype,
            "guests": guests,
            "revenue": revenue,
            "cost": cost,
            "margin": round(revenue - cost, 2),
            "status": status,
            "paid": bool(realized and rng.random() < 0.78),
            "nps": int(rng.integers(6, 11)) if realized and rng.random() < 0.9 else np.nan,
            "on_time": bool(rng.random() < 0.88) if realized else None,
            "delivery_km": round(float(rng.uniform(8, 130)), 1),
            "vehicle": str(rng.choice(VEHICLES)),
            "driver": str(rng.choice(DRIVERS)),
            "items_count": int(rng.integers(40, 420)),
        })
    events = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    inventory = _build_inventory(rng)
    return CompanyData(events=events, inventory=inventory, clients=clients,
                       as_of=pd.Timestamp(today))


def _recurrence_weights(rng: np.random.Generator, n: int) -> np.ndarray:
    # A few clients are very frequent (long tail), like a real book of business.
    weights = rng.pareto(2.0, size=n) + 0.2
    return weights / weights.sum()


def _build_inventory(rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for item, category, total in _ITEM_CATALOG:
        rented = int(total * float(rng.uniform(0.35, 0.85)))
        maintenance = int(total * float(rng.uniform(0.0, 0.08)))
        available = max(total - rented - maintenance, 0)
        rows.append({
            "item": item, "category": category, "total": total,
            "rented": rented, "maintenance": maintenance, "available": available,
            "utilization": rented / total if total else 0.0,
        })
    return pd.DataFrame(rows)
