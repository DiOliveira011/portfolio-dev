"""Deterministic synthetic sales at (mês, categoria, região, canal) grain."""

from __future__ import annotations

import math
import random

N_MESES = 18
CATEGORIAS = {"Eletrônicos": 0.40, "Casa": 0.25, "Esporte": 0.20, "Livros": 0.15}
REGIOES = {"Sudeste": 0.45, "Sul": 0.20, "Nordeste": 0.18, "Centro-Oeste": 0.10, "Norte": 0.07}
# Crescimento/queda por categoria ao longo do tempo (gera a narrativa).
_CAT_TREND = {"Esporte": 0.013, "Livros": -0.011}


def month_labels(n: int = N_MESES, start_year: int = 2025, start_month: int = 1) -> list[str]:
    labels = []
    y, m = start_year, start_month
    for _ in range(n):
        labels.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return labels


def generate_sales(seed: int = 11) -> list[dict]:
    """Return a list of monthly sales rows with an upward trend + seasonality."""
    rng = random.Random(seed)
    labels = month_labels()
    rows: list[dict] = []
    for m, label in enumerate(labels):
        seasonal = 1.0 + 0.16 * math.sin((m % 12) / 12 * 2 * math.pi - 0.6)
        if (m % 12) in (10, 11):           # nov/dez aquecem
            seasonal += 0.12
        total = 100_000 * (1.02 ** m) * seasonal * rng.uniform(0.96, 1.04)
        ecom = min(0.25 + 0.012 * m, 0.60)  # e-commerce cresce com o tempo
        canais = {"E-commerce": ecom,
                  "Loja física": (1 - ecom) * 0.78,
                  "Marketplace": (1 - ecom) * 0.22}
        for cat, base_share in CATEGORIAS.items():
            cat_adj = base_share * (1 + _CAT_TREND.get(cat, 0.0) * m)
            for reg, rshare in REGIOES.items():
                for canal, cshare in canais.items():
                    valor = total * cat_adj * rshare * cshare * rng.uniform(0.9, 1.1)
                    rows.append({"mes": label, "categoria": cat, "regiao": reg,
                                 "canal": canal, "valor": round(valor, 2)})
    return rows
