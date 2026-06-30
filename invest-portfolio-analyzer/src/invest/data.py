"""Price data: synthetic generation (offline) and optional live fetch.

Canonical output: a wide DataFrame indexed by date, one column of adjusted
close prices per ticker.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

#: Demo tickers with plausible annual drift/volatility for synthetic prices.
_SAMPLE_ASSETS: dict[str, tuple[float, float]] = {
    "PETR4": (0.12, 0.34),
    "VALE3": (0.10, 0.30),
    "ITUB4": (0.14, 0.25),
    "WEGE3": (0.18, 0.28),
    "MGLU3": (0.05, 0.55),
    "IBOV": (0.11, 0.18),   # benchmark-like
}


def generate_sample_prices(
    *, days: int = 756, seed: int = 42, start: float = 100.0
) -> pd.DataFrame:
    """Generate ~3 years of daily prices via geometric Brownian motion."""
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=days)
    cols: dict[str, np.ndarray] = {}
    for ticker, (mu, sigma) in _SAMPLE_ASSETS.items():
        dt = 1 / 252
        shocks = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), size=days)
        cols[ticker] = start * np.exp(np.cumsum(shocks))
    return pd.DataFrame(cols, index=dates)


def fetch_prices(tickers: list[str], period: str = "3y") -> pd.DataFrame:
    """Fetch adjusted close prices via yfinance (optional dependency).

    Raises a clear error if yfinance is not installed or returns nothing.
    """
    try:
        import yfinance as yf
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "yfinance não está instalado. Use os dados de exemplo ou "
            "`pip install yfinance`."
        ) from exc

    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)
    closes = data.get("Close", data)
    closes = closes.dropna(how="all").ffill().dropna()
    if closes.empty:
        raise RuntimeError("Nenhum dado retornado para os tickers informados.")
    return closes


def sample_tickers() -> list[str]:
    return list(_SAMPLE_ASSETS)
