"""Service layer: build base, train once, score everyone, compute KPIs."""

from __future__ import annotations

from churn.data import generate_customers
from churn.model import risk_band, score_one, train


class ChurnService:
    """Holds the synthetic base + trained model and exposes the cockpit data."""

    def __init__(self, n: int = 800, seed: int = 42) -> None:
        self.customers = generate_customers(n=n, seed=seed)
        trained = train(self.customers, seed=seed)
        self.model = trained["model"]
        self.metrics = trained["metrics"]
        self.importances = trained["importances"]
        for c in self.customers:
            c["risco"] = score_one(self.model, c)
            c["banda"] = risk_band(c["risco"])

    def kpis(self) -> dict:
        total = len(self.customers)
        ativos = [c for c in self.customers if not c["churn"]]
        em_risco = [c for c in ativos if c["risco"] >= 0.6]
        receita_ativa = sum(c["mensalidade"] for c in ativos)
        receita_risco = sum(c["mensalidade"] for c in em_risco)
        churned = sum(c["churn"] for c in self.customers)
        return {
            "total": total,
            "churn_rate": churned / total if total else 0.0,
            "ativos": len(ativos),
            "em_risco": len(em_risco),
            "receita_ativa": receita_ativa,
            "receita_risco": receita_risco,
            "ticket_medio": receita_ativa / len(ativos) if ativos else 0.0,
        }

    def top_risco(self, n: int = 25) -> list[dict]:
        ativos = [c for c in self.customers if not c["churn"]]
        return sorted(ativos, key=lambda c: c["risco"], reverse=True)[:n]

    def simulate(self, payload: dict) -> dict:
        prob = score_one(self.model, payload)
        return {"risco": prob, "banda": risk_band(prob)}
