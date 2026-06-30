"""Generate realistic synthetic statement data for demos and tests.

Deterministic (seeded) so the demo and tests are reproducible.
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

# Merchant pools per category (align with KEYWORD_RULES so rules pick them up).
_EXPENSE_MERCHANTS: dict[str, list[str]] = {
    "Mercado": ["Supermercado Pao de Acucar", "Carrefour", "Assai Atacadista", "Hortifruti"],
    "Alimentação": ["iFood *Restaurante", "Padaria Sao Joao", "McDonalds", "Starbucks Cafe"],
    "Transporte": ["Uber *Trip", "99app", "Posto Ipiranga", "Estacionamento Shopping"],
    "Moradia": ["Aluguel Imobiliaria", "Enel Energia", "Sabesp Agua", "Vivo Fibra Internet"],
    "Saúde": ["Drogaria Raia", "Farmacia Pacheco", "Unimed", "Clinica Odontologica"],
    "Lazer": ["Cinemark", "Steam Games", "Ingresso Show", "Spotify"],
    "Compras": ["Amazon.com.br", "Mercado Livre", "Magazine Luiza", "Shopee"],
    "Assinaturas": ["Netflix", "Amazon Prime", "Google One", "Microsoft 365"],
}
_INCOME_SOURCES = ["Salario Empresa XPTO", "Pagamento Freelance", "Restituicao IR"]


def generate_sample_dataframe(*, months: int = 3, seed: int = 42) -> pd.DataFrame:
    """Return a canonical transactions DataFrame with synthetic data."""
    rng = random.Random(seed)
    today = date.today()
    start = today - timedelta(days=months * 30)
    rows: list[dict[str, object]] = []

    current = start.replace(day=1)
    for _ in range(months):
        # One salary per month (kept comfortably above expenses for a healthy demo).
        rows.append(
            {
                "date": current + timedelta(days=4),
                "description": rng.choice(_INCOME_SOURCES),
                "amount": round(rng.uniform(7500, 9500), 2),
            }
        )
        # A fixed monthly rent.
        rows.append(
            {
                "date": current + timedelta(days=9),
                "description": "Aluguel Imobiliaria",
                "amount": -round(rng.uniform(1400, 1700), 2),
            }
        )
        # A spread of everyday expenses across the month.
        for _ in range(rng.randint(16, 24)):
            category = rng.choice(list(_EXPENSE_MERCHANTS))
            merchant = rng.choice(_EXPENSE_MERCHANTS[category])
            day = rng.randint(1, 27)
            value = _amount_for(category, rng)
            rows.append(
                {
                    "date": current + timedelta(days=day - 1),
                    "description": merchant,
                    "amount": -value,
                }
            )
        current = _next_month(current)

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def _amount_for(category: str, rng: random.Random) -> float:
    ranges = {
        "Mercado": (40, 320),
        "Alimentação": (15, 110),
        "Transporte": (8, 80),
        "Moradia": (60, 350),
        "Saúde": (20, 250),
        "Lazer": (15, 150),
        "Compras": (25, 400),
        "Assinaturas": (10, 60),
    }
    low, high = ranges.get(category, (10, 200))
    return round(rng.uniform(low, high), 2)


def _next_month(d: date) -> date:
    return date(d.year + 1, 1, 1) if d.month == 12 else date(d.year, d.month + 1, 1)


def write_sample_csv(path: str | Path, *, months: int = 3, seed: int = 42) -> Path:
    """Write a Brazilian-formatted CSV (Data; Histórico; Valor) and return its path."""
    df = generate_sample_dataframe(months=months, seed=seed)
    out = pd.DataFrame(
        {
            "Data": df["date"].dt.strftime("%d/%m/%Y"),
            "Histórico": df["description"],
            "Valor": df["amount"].map(lambda v: f"{v:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")),
        }
    )
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(target, index=False, sep=";", encoding="utf-8-sig")
    return target


if __name__ == "__main__":
    written = write_sample_csv(
        Path(__file__).resolve().parents[2] / "sample_data" / "extrato_exemplo.csv"
    )
    print(f"Wrote {written}")
