"""KPIs and aggregations computed over a categorized transactions DataFrame.

Every function expects the canonical schema: ``date`` (datetime64),
``description`` (str), ``amount`` (float, signed) and ``category`` (str).
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class Summary:
    """Headline KPIs for a set of transactions."""

    income: float
    expense: float
    net: float
    savings_rate: float
    transactions: int
    months: int
    avg_monthly_expense: float


def summary(df: pd.DataFrame) -> Summary:
    """Compute headline KPIs."""
    if df.empty:
        return Summary(0.0, 0.0, 0.0, 0.0, 0, 0, 0.0)

    income = float(df.loc[df["amount"] > 0, "amount"].sum())
    expense = float(-df.loc[df["amount"] < 0, "amount"].sum())
    net = income - expense
    savings_rate = (net / income) if income > 0 else 0.0
    months = max(1, df["date"].dt.to_period("M").nunique())
    return Summary(
        income=income,
        expense=expense,
        net=net,
        savings_rate=savings_rate,
        transactions=int(len(df)),
        months=int(months),
        avg_monthly_expense=expense / months,
    )


def by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Expense total per category (descending), with share of total."""
    expenses = df[df["amount"] < 0]
    if expenses.empty:
        return pd.DataFrame(columns=["category", "total", "share"])
    grouped = (
        expenses.assign(total=expenses["amount"].abs())
        .groupby("category", as_index=False)["total"]
        .sum()
        .sort_values("total", ascending=False)
        .reset_index(drop=True)
    )
    grand_total = grouped["total"].sum()
    grouped["share"] = grouped["total"] / grand_total if grand_total else 0.0
    return grouped


def by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly income, expense and net."""
    if df.empty:
        return pd.DataFrame(columns=["month", "income", "expense", "net"])
    work = df.assign(month=df["date"].dt.to_period("M").astype(str))
    income = work[work["amount"] > 0].groupby("month")["amount"].sum()
    expense = work[work["amount"] < 0].groupby("month")["amount"].sum().abs()
    out = pd.DataFrame({"income": income, "expense": expense}).fillna(0.0)
    out["net"] = out["income"] - out["expense"]
    return out.reset_index().sort_values("month").reset_index(drop=True)


def top_expenses(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """The ``n`` largest individual expenses."""
    expenses = df[df["amount"] < 0]
    if expenses.empty:
        return pd.DataFrame(columns=["date", "description", "category", "amount"])
    return (
        expenses.assign(amount=expenses["amount"].abs())
        .sort_values("amount", ascending=False)
        .head(n)[["date", "description", "category", "amount"]]
        .reset_index(drop=True)
    )
