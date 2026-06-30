"""Tests for portfolio analytics."""

from __future__ import annotations

import numpy as np
import pandas as pd

from invest.portfolio import (
    compute_metrics,
    correlation,
    daily_returns,
    max_sharpe_portfolio,
    portfolio_returns,
    random_portfolios,
)


def _returns() -> pd.DataFrame:
    idx = pd.bdate_range("2024-01-01", periods=60)
    rng = np.random.default_rng(0)
    return pd.DataFrame(
        {
            "A": rng.normal(0.001, 0.010, 60),
            "B": rng.normal(0.0005, 0.012, 60),
        },
        index=idx,
    )


def test_daily_returns_shape() -> None:
    prices = pd.DataFrame({"A": [10, 11, 12], "B": [5, 5, 6]})
    assert len(daily_returns(prices)) == 2


def test_portfolio_returns_equal_weight() -> None:
    r = _returns()
    p = portfolio_returns(r, [1, 1])
    expected = (r["A"] + r["B"]) / 2
    assert np.allclose(p.to_numpy(), expected.to_numpy())


def test_metrics_on_constant_growth() -> None:
    idx = pd.bdate_range("2024-01-01", periods=30)
    series = pd.Series([0.005] * 30, index=idx)
    m = compute_metrics(series)
    assert m.ann_return > 0
    assert m.ann_vol < 1e-9            # constant returns -> ~zero volatility
    assert abs(m.max_drawdown) < 1e-9  # never below the running peak
    assert m.total_return > 0


def test_random_portfolios_valid() -> None:
    r = _returns()
    cloud = random_portfolios(r, n=300, seed=2)
    weights_sum = cloud[["A", "B"]].sum(axis=1)
    assert np.allclose(weights_sum.to_numpy(), 1.0)
    nonzero = cloud[cloud["vol"] > 0]
    assert np.allclose((nonzero["ret"] / nonzero["vol"]).to_numpy(), nonzero["sharpe"].to_numpy())
    assert max_sharpe_portfolio(cloud)["sharpe"] == cloud["sharpe"].max()


def test_correlation_diagonal_is_one() -> None:
    c = correlation(_returns())
    assert np.allclose(np.diag(c.to_numpy()), 1.0)
