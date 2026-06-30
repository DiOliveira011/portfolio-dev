"""Invest Portfolio Analyzer — Streamlit app. Run with: streamlit run app.py"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import numpy as np  # noqa: E402
import plotly.express as px  # noqa: E402
import streamlit as st  # noqa: E402

from invest.data import fetch_prices, generate_sample_prices  # noqa: E402
from invest.portfolio import (  # noqa: E402
    TRADING_DAYS,
    compute_metrics,
    correlation,
    cumulative_curve,
    daily_returns,
    max_sharpe_portfolio,
    portfolio_returns,
    random_portfolios,
)

st.set_page_config(page_title="Invest Portfolio Analyzer", page_icon="📈", layout="wide")


def _load_prices():
    st.sidebar.title("📈 Portfolio Analyzer")
    source = st.sidebar.radio("Fonte de dados", ["Dados de exemplo", "Buscar (yfinance)"])
    if source == "Buscar (yfinance)":
        raw = st.sidebar.text_input(
            "Tickers (separados por vírgula)", "PETR4.SA, VALE3.SA, ITUB4.SA"
        )
        period = st.sidebar.selectbox("Período", ["1y", "2y", "3y", "5y"], index=2)
        if st.sidebar.button("Buscar preços", use_container_width=True):
            try:
                tickers = [t.strip() for t in raw.split(",") if t.strip()]
                st.session_state["prices"] = fetch_prices(tickers, period)
            except Exception as exc:  # noqa: BLE001
                st.sidebar.error(str(exc))
    elif "prices" not in st.session_state:
        st.session_state["prices"] = generate_sample_prices()
    if st.sidebar.button("↺ Recarregar exemplo", use_container_width=True):
        st.session_state["prices"] = generate_sample_prices()


def main() -> None:
    _load_prices()
    st.title("📈 Análise de Carteira")

    if "prices" not in st.session_state:
        st.info("👈 Carregue os dados de exemplo ou busque tickers para começar.")
        return

    prices = st.session_state["prices"]
    returns = daily_returns(prices)
    assets = list(prices.columns)

    benchmark = st.sidebar.selectbox("Benchmark", assets, index=len(assets) - 1)
    portfolio_assets = [a for a in assets if a != benchmark]

    st.sidebar.markdown("**Pesos da carteira (%)**")
    default = 100.0 / len(portfolio_assets)
    weights = [
        st.sidebar.number_input(a, 0.0, 100.0, round(default, 1), step=5.0, key=f"w_{a}")
        for a in portfolio_assets
    ]
    if sum(weights) <= 0:
        st.warning("Defina pesos positivos para a carteira.")
        return

    asset_returns = returns[portfolio_assets]
    port = portfolio_returns(asset_returns, weights)
    bench = returns[benchmark]

    pm = compute_metrics(port)
    bm = compute_metrics(bench)

    st.caption(
        f"{len(prices)} pregões · {len(portfolio_assets)} ativos · "
        f"benchmark **{benchmark}**"
    )
    delta_vs_bench = f"{(pm.ann_return - bm.ann_return) * 100:.1f}pp vs bench"
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Retorno anual.", f"{pm.ann_return * 100:.1f}%", delta_vs_bench)
    c2.metric("Volatilidade", f"{pm.ann_vol * 100:.1f}%")
    c3.metric("Sharpe", f"{pm.sharpe:.2f}")
    c4.metric("Máx. drawdown", f"{pm.max_drawdown * 100:.1f}%")
    c5.metric("Retorno total", f"{pm.total_return * 100:.1f}%")

    # Cumulative returns: portfolio vs benchmark.
    st.subheader("Retorno acumulado")
    curve = (
        cumulative_curve(port).rename("Carteira").to_frame()
        .join(cumulative_curve(bench).rename(benchmark))
    )
    fig = px.line(curve, color_discrete_sequence=["#10b981", "#f59e0b"])
    fig.update_layout(xaxis_title="", yaxis_title="Crescimento de R$ 1", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    # Correlation heatmap.
    with left:
        st.subheader("Correlação")
        corr = correlation(returns)
        heat = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu", zmin=-1, zmax=1)
        heat.update_layout(margin={"t": 10})
        st.plotly_chart(heat, use_container_width=True)

    # Efficient frontier (Monte Carlo).
    with right:
        st.subheader("Fronteira eficiente (Monte Carlo)")
        cloud = random_portfolios(asset_returns, n=3000, seed=1)
        best = max_sharpe_portfolio(cloud)
        scatter = px.scatter(
            cloud, x="vol", y="ret", color="sharpe", color_continuous_scale="Viridis",
            labels={"vol": "Volatilidade", "ret": "Retorno", "sharpe": "Sharpe"},
        )
        # Current portfolio point.
        w = np.asarray(weights, dtype=float)
        w = w / w.sum()
        cur_ret = float(w @ (asset_returns.mean().to_numpy() * TRADING_DAYS))
        cur_vol = float(np.sqrt(w @ (asset_returns.cov().to_numpy() * TRADING_DAYS) @ w))
        scatter.add_scatter(
            x=[cur_vol], y=[cur_ret], mode="markers", name="Sua carteira",
            marker={"size": 14, "color": "#10b981", "symbol": "star"},
        )
        scatter.add_scatter(
            x=[best["vol"]], y=[best["ret"]], mode="markers", name="Máx. Sharpe",
            marker={"size": 14, "color": "#ef4444", "symbol": "diamond"},
        )
        st.plotly_chart(scatter, use_container_width=True)

    st.caption(
        "Carteira de **máximo Sharpe** sugerida: "
        + " · ".join(f"{a} {best[a] * 100:.0f}%" for a in portfolio_assets)
    )

    st.info("Ferramenta educacional — não é recomendação de investimento.")


if __name__ == "__main__":
    main()
