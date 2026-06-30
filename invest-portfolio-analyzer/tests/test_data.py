"""Tests for price data generation."""

from __future__ import annotations

from invest.data import generate_sample_prices, sample_tickers


def test_generate_sample_prices() -> None:
    prices = generate_sample_prices(days=120, seed=1)
    assert len(prices) == 120
    assert list(prices.columns) == sample_tickers()
    assert (prices > 0).all().all()
