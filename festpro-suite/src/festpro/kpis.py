"""KPI calculations and aggregations over the company dataset.

Every function is pure (DataFrame in, DataFrame/dict out) so the pages stay thin
and the metrics are unit-testable.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from festpro.data import CompanyData


def realized(events: pd.DataFrame) -> pd.DataFrame:
    return events[events["status"] == "Realizado"]


def past(events: pd.DataFrame, as_of: pd.Timestamp) -> pd.DataFrame:
    return events[events["date"] <= as_of]


@dataclass(slots=True)
class Overview:
    """Headline KPIs for the executive page."""

    revenue_month: float
    revenue_delta: float          # vs previous month (fraction)
    events_month: int
    avg_ticket: float
    conversion: float
    nps: float
    on_time: float
    inventory_util: float
    receivables: float
    backlog: float                # confirmed future revenue


def overview(data: CompanyData) -> Overview:
    """Compute the executive headline KPIs."""
    ev, as_of = data.events, data.as_of
    month_start = as_of.replace(day=1)
    prev_start = (month_start - pd.Timedelta(days=1)).replace(day=1)

    real = realized(ev)
    this_month = real[(real["date"] >= month_start) & (real["date"] <= as_of)]
    prev_month = real[(real["date"] >= prev_start) & (real["date"] < month_start)]

    rev_month = float(this_month["revenue"].sum())
    rev_prev = float(prev_month["revenue"].sum())
    delta = (rev_month - rev_prev) / rev_prev if rev_prev else 0.0

    closed = past(ev, as_of)
    decided = closed[closed["status"].isin(["Realizado", "Cancelado", "Orçamento"])]
    conversion = (decided["status"] == "Realizado").mean() if len(decided) else 0.0

    backlog = float(ev[(ev["status"] == "Confirmado") & (ev["date"] > as_of)]["revenue"].sum())

    return Overview(
        revenue_month=rev_month,
        revenue_delta=delta,
        events_month=int(len(this_month)),
        avg_ticket=(rev_month / len(this_month)) if len(this_month) else 0.0,
        conversion=float(conversion),
        nps=float(real["nps"].mean()) if real["nps"].notna().any() else 0.0,
        on_time=float(real["on_time"].dropna().mean()) if real["on_time"].notna().any() else 0.0,
        inventory_util=float(data.inventory["rented"].sum() / data.inventory["total"].sum()),
        receivables=float(real[~real["paid"]]["revenue"].sum()),
        backlog=backlog,
    )


def revenue_by_month(events: pd.DataFrame, *, months: int = 12) -> pd.DataFrame:
    real = realized(events).copy()
    real["month"] = real["date"].dt.to_period("M").astype(str)
    out = real.groupby("month", as_index=False)["revenue"].sum()
    return out.sort_values("month").tail(months).reset_index(drop=True)


def finance_monthly(events: pd.DataFrame, *, months: int = 12) -> pd.DataFrame:
    real = realized(events).copy()
    real["month"] = real["date"].dt.to_period("M").astype(str)
    out = real.groupby("month", as_index=False)[["revenue", "cost", "margin"]].sum()
    return out.sort_values("month").tail(months).reset_index(drop=True)


def by_type(events: pd.DataFrame) -> pd.DataFrame:
    real = realized(events)
    out = real.groupby("type", as_index=False).agg(
        eventos=("event_id", "count"), receita=("revenue", "sum")
    )
    return out.sort_values("receita", ascending=False).reset_index(drop=True)


def by_region(events: pd.DataFrame) -> pd.DataFrame:
    real = realized(events)
    out = real.groupby("region", as_index=False)["revenue"].sum()
    return out.sort_values("revenue", ascending=False).reset_index(drop=True)


def funnel(events: pd.DataFrame, as_of: pd.Timestamp) -> pd.DataFrame:
    closed = past(events, as_of)
    counts = {
        "Orçamentos": int(len(closed)),  # every event starts as a quote
        "Confirmados": int(closed["status"].isin(["Confirmado", "Realizado"]).sum()),
        "Realizados": int((closed["status"] == "Realizado").sum()),
    }
    return pd.DataFrame({"etapa": list(counts), "quantidade": list(counts.values())})


def top_clients(events: pd.DataFrame, *, n: int = 10) -> pd.DataFrame:
    real = realized(events)
    out = real.groupby(["client", "segment"], as_index=False).agg(
        eventos=("event_id", "count"), receita=("revenue", "sum")
    )
    return out.sort_values("receita", ascending=False).head(n).reset_index(drop=True)


def upcoming_events(events: pd.DataFrame, as_of: pd.Timestamp, *, n: int = 15) -> pd.DataFrame:
    fut = events[(events["date"] > as_of) & (events["status"].isin(["Confirmado", "Orçamento"]))]
    cols = ["date", "client", "type", "region", "guests", "revenue", "status"]
    return fut.sort_values("date").head(n)[cols].reset_index(drop=True)


def receivables_aging(events: pd.DataFrame, as_of: pd.Timestamp) -> pd.DataFrame:
    real = realized(events)
    unpaid = real[~real["paid"]].copy()
    unpaid["dias"] = (as_of - unpaid["date"]).dt.days
    bins = [-1, 30, 60, 90, 10_000]
    labels = ["0–30 dias", "31–60 dias", "61–90 dias", "90+ dias"]
    unpaid["faixa"] = pd.cut(unpaid["dias"], bins=bins, labels=labels)
    out = unpaid.groupby("faixa", as_index=False, observed=True)["revenue"].sum()
    return out.rename(columns={"revenue": "valor"})


def deliveries_by_driver(events: pd.DataFrame) -> pd.DataFrame:
    real = realized(events)
    out = real.groupby("driver", as_index=False).agg(
        entregas=("event_id", "count"),
        km=("delivery_km", "sum"),
        no_prazo=("on_time", "mean"),
    )
    return out.sort_values("km", ascending=False).reset_index(drop=True)
