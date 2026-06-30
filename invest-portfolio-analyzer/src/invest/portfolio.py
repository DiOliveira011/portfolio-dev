"""Portfolio analytics: returns, risk metrics and a Monte Carlo frontier."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd

TRADING_DAYS = 252


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Simple daily returns, dropping the first (NaN) row."""
    return prices.pct_change(fill_method=None).dropna(how="any")


def portfolio_returns(returns: pd.DataFrame, weights: np.ndarray | list[float]) -> pd.Series:
    """Weighted daily return series for a portfolio (weights are normalized)."""
    w = np.asarray(weights, dtype=float)
    total = w.sum()
    if total <= 0:
        raise ValueError("A soma dos pesos deve ser positiva.")
    w = w / total
    return pd.Series(returns.to_numpy() @ w, index=returns.index, name="portfolio")


@dataclass(slots=True)
class Metrics:
    """Headline risk/return metrics (annualized where relevant)."""

    ann_return: float
    ann_vol: float
    sharpe: float
    max_drawdown: float
    total_return: float


def compute_metrics(returns: pd.Series, *, risk_free: float = 0.0) -> Metrics:
    """Annualized return/vol, Sharpe, max drawdown and total return."""
    if returns.empty:
        return Metrics(0.0, 0.0, 0.0, 0.0, 0.0)
    mean = float(returns.mean())
    std = float(returns.std(ddof=1))
    ann_return = (1 + mean) ** TRADING_DAYS - 1
    ann_vol = std * math.sqrt(TRADING_DAYS)
    sharpe = (ann_return - risk_free) / ann_vol if ann_vol > 0 else 0.0
    curve = cumulative_curve(returns)
    total_return = float(curve.iloc[-1] - 1)
    max_drawdown = float((curve / curve.cummax() - 1).min())
    return Metrics(ann_return, ann_vol, sharpe, max_drawdown, total_return)


def cumulative_curve(returns: pd.Series) -> pd.Series:
    """Growth of 1 unit invested (cumulative product of (1 + r))."""
    return (1 + returns).cumprod()


def correlation(returns: pd.DataFrame) -> pd.DataFrame:
    return returns.corr()


def random_portfolios(returns: pd.DataFrame, *, n: int = 4000, seed: int = 0) -> pd.DataFrame:
    """Monte Carlo of random long-only portfolios → risk/return/Sharpe cloud."""
    rng = np.random.default_rng(seed)
    assets = list(returns.columns)
    mean_annual = returns.mean().to_numpy() * TRADING_DAYS
    cov_annual = returns.cov().to_numpy() * TRADING_DAYS

    rows: list[list[float]] = []
    for _ in range(n):
        w = rng.random(len(assets))
        w /= w.sum()
        ret = float(w @ mean_annual)
        vol = float(np.sqrt(w @ cov_annual @ w))
        sharpe = ret / vol if vol > 0 else 0.0
        rows.append([ret, vol, sharpe, *w])
    return pd.DataFrame(rows, columns=["ret", "vol", "sharpe", *assets])


def max_sharpe_portfolio(frontier: pd.DataFrame) -> pd.Series:
    """Row of the random-portfolio cloud with the highest Sharpe ratio."""
    return frontier.loc[frontier["sharpe"].idxmax()]
