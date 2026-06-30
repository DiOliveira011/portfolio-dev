"""Synthetic (but realistic) customer base for a subscription business.

Deterministic given a seed — the "case" comes pre-carregado, sem CSV para subir.
"""

from __future__ import annotations

import numpy as np

CONTRATOS = ["Mensal", "Anual", "Bienal"]
CONTRATO_ORD = {nome: i for i, nome in enumerate(CONTRATOS)}
PLANOS = {"Básico": 49.9, "Pró": 99.9, "Premium": 169.9}

FEATURES = [
    "tenure_meses", "mensalidade", "contrato_ord",
    "suporte_chamados", "atraso_pagamento", "uso_gb",
]
FEATURE_LABELS = {
    "tenure_meses": "Tempo de casa (meses)",
    "mensalidade": "Mensalidade (R$)",
    "contrato_ord": "Tipo de contrato",
    "suporte_chamados": "Chamados ao suporte",
    "atraso_pagamento": "Atraso de pagamento",
    "uso_gb": "Uso de dados (GB)",
}

_FIRST = ["Ana", "Bruno", "Carla", "Diego", "Elaine", "Felipe", "Gabriela", "Hugo",
          "Isabela", "João", "Karina", "Lucas", "Marina", "Nelson", "Olívia", "Paulo",
          "Quésia", "Rafael", "Sofia", "Tiago", "Úrsula", "Vinícius", "Wagner", "Yara"]
_LAST = ["Silva", "Souza", "Costa", "Pereira", "Almeida", "Lima", "Gomes", "Ribeiro",
         "Carvalho", "Araújo", "Barbosa", "Rocha", "Martins", "Nascimento", "Moreira"]


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-z))


def generate_customers(n: int = 800, seed: int = 42) -> list[dict]:
    """Return ``n`` customers with a realistic latent churn signal."""
    rng = np.random.default_rng(seed)
    customers: list[dict] = []
    for i in range(n):
        contrato = CONTRATOS[rng.choice(3, p=[0.55, 0.30, 0.15])]
        plano_nome = list(PLANOS)[rng.choice(3, p=[0.45, 0.35, 0.20])]
        mensalidade = round(PLANOS[plano_nome] + rng.normal(0, 6), 2)
        tenure = int(np.clip(rng.gamma(2.2, 9.0), 1, 72))
        chamados = int(rng.poisson(1.6))
        atraso = int(rng.random() < 0.18)
        uso_gb = round(float(np.clip(rng.normal(28, 12), 1, 90)), 1)

        z = (-0.7
             - 0.060 * tenure
             + 0.012 * (mensalidade - 100)
             + 0.38 * chamados
             + 1.60 * atraso
             + {"Mensal": 1.1, "Anual": -0.5, "Bienal": -1.6}[contrato]
             + rng.normal(0, 0.25))
        churn = int(rng.random() < float(_sigmoid(np.array(z))))

        customers.append({
            "id": f"C{i + 1:04d}",
            "nome": f"{_FIRST[rng.integers(len(_FIRST))]} {_LAST[rng.integers(len(_LAST))]}",
            "plano": plano_nome,
            "contrato": contrato,
            "contrato_ord": CONTRATO_ORD[contrato],
            "tenure_meses": tenure,
            "mensalidade": mensalidade,
            "suporte_chamados": chamados,
            "atraso_pagamento": atraso,
            "uso_gb": uso_gb,
            "churn": churn,
        })
    return customers


def to_xy(customers: list[dict]) -> tuple[np.ndarray, np.ndarray]:
    x = np.array([[c[f] for f in FEATURES] for c in customers], dtype=float)
    y = np.array([c["churn"] for c in customers], dtype=int)
    return x, y
