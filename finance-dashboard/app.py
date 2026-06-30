"""Finance Dashboard — Streamlit app.

Run with:  streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make ``src`` importable when running via ``streamlit run app.py``.
_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import pandas as pd  # noqa: E402
import plotly.express as px  # noqa: E402
import streamlit as st  # noqa: E402

from findash.analysis import by_category, by_month, summary, top_expenses  # noqa: E402
from findash.categorize import categorize_dataframe  # noqa: E402
from findash.core.categories import CATEGORIES  # noqa: E402
from findash.ingest import load_transactions  # noqa: E402
from findash.sample import generate_sample_dataframe  # noqa: E402
from findash.utils.formatting import format_currency  # noqa: E402

# A varied, qualitative palette (not the black/green Orc theme).
_PALETTE = px.colors.qualitative.Bold

st.set_page_config(page_title="Finance Dashboard", page_icon="💸", layout="wide")


# --- Data loading ----------------------------------------------------------
def _load_into_state(df: pd.DataFrame, *, use_ml: bool) -> None:
    result = categorize_dataframe(df, use_ml=use_ml)
    st.session_state["data"] = result.df
    st.session_state["stats"] = result


def _sidebar() -> None:
    st.sidebar.title("💸 Finance Dashboard")
    st.sidebar.caption("Importe um extrato, categorize e visualize.")

    use_ml = st.sidebar.toggle("Categorizar com IA (ML)", value=True)
    uploaded = st.sidebar.file_uploader(
        "Extrato (CSV ou OFX)", type=["csv", "ofx", "qfx"]
    )
    if uploaded is not None:
        try:
            df = load_transactions(uploaded, uploaded.name)
            _load_into_state(df, use_ml=use_ml)
            st.sidebar.success(f"{len(df)} transações carregadas.")
        except Exception as exc:  # noqa: BLE001 - surface friendly error
            st.sidebar.error(f"Não consegui ler o arquivo: {exc}")

    if st.sidebar.button("✨ Usar dados de exemplo", use_container_width=True):
        _load_into_state(generate_sample_dataframe(), use_ml=use_ml)

    if "data" in st.session_state:
        st.sidebar.divider()
        st.sidebar.caption("Dica: edite categorias na tabela ao final da página.")


# --- Rendering -------------------------------------------------------------
def _render_kpis(df: pd.DataFrame) -> None:
    s = summary(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Entradas", format_currency(s.income))
    c2.metric("Saídas", format_currency(s.expense))
    c3.metric("Saldo", format_currency(s.net))
    c4.metric("Taxa de poupança", f"{s.savings_rate * 100:.0f}%")
    st.caption(
        f"{s.transactions} transações · {s.months} mês(es) · "
        f"gasto médio mensal {format_currency(s.avg_monthly_expense)}"
    )


def _render_charts(df: pd.DataFrame) -> None:
    left, right = st.columns(2)

    cats = by_category(df)
    if not cats.empty:
        fig = px.bar(
            cats, x="total", y="category", orientation="h",
            color="category", color_discrete_sequence=_PALETTE,
            title="Despesas por categoria",
        )
        fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="R$")
        left.plotly_chart(fig, use_container_width=True)

    months = by_month(df)
    if not months.empty:
        melted = months.melt(
            id_vars="month", value_vars=["income", "expense"],
            var_name="tipo", value_name="valor",
        ).replace({"income": "Entradas", "expense": "Saídas"})
        fig2 = px.bar(
            melted, x="month", y="valor", color="tipo", barmode="group",
            color_discrete_sequence=[_PALETTE[2], _PALETTE[0]],
            title="Fluxo mensal",
        )
        fig2.update_layout(xaxis_title="", yaxis_title="R$", legend_title="")
        right.plotly_chart(fig2, use_container_width=True)

    # Cumulative balance over time.
    balance = df.sort_values("date").assign(saldo=lambda d: d["amount"].cumsum())
    fig3 = px.area(
        balance, x="date", y="saldo", title="Saldo acumulado",
        color_discrete_sequence=[_PALETTE[4]],
    )
    fig3.update_layout(xaxis_title="", yaxis_title="R$")
    st.plotly_chart(fig3, use_container_width=True)


def _render_top_and_editor(df: pd.DataFrame, *, use_ml: bool) -> None:
    st.subheader("Maiores despesas")
    top = top_expenses(df, n=10)
    if not top.empty:
        view = top.copy()
        view["amount"] = view["amount"].map(format_currency)
        view["date"] = view["date"].dt.strftime("%d/%m/%Y")
        st.dataframe(
            view.rename(
                columns={
                    "date": "Data", "description": "Descrição",
                    "category": "Categoria", "amount": "Valor",
                }
            ),
            use_container_width=True, hide_index=True,
        )

    st.subheader("Revisar e ajustar categorias")
    editable = df[["date", "description", "amount", "category"]].copy()
    edited = st.data_editor(
        editable,
        use_container_width=True, hide_index=True, height=320,
        column_config={
            "date": st.column_config.DateColumn("Data", disabled=True),
            "description": st.column_config.TextColumn("Descrição", disabled=True),
            "amount": st.column_config.NumberColumn("Valor", disabled=True, format="R$ %.2f"),
            "category": st.column_config.SelectboxColumn("Categoria", options=CATEGORIES),
        },
    )
    if not edited["category"].equals(df["category"]):
        st.session_state["data"] = edited
        st.rerun()


def main() -> None:
    _sidebar()
    st.title("Painel de Finanças Pessoais")

    if "data" not in st.session_state:
        st.info(
            "👈 Importe um extrato (CSV/OFX) na barra lateral ou clique em "
            "**Usar dados de exemplo** para começar."
        )
        with st.expander("Como funciona"):
            st.markdown(
                "- **Importa** seu extrato e normaliza datas/valores (formatos BR e US).\n"
                "- **Categoriza** com regras + um modelo de ML que aprende com as regras.\n"
                "- **Visualiza** KPIs, despesas por categoria, fluxo mensal e saldo.\n"
                "- **Ajuste** qualquer categoria na tabela — tudo recalcula na hora."
            )
        return

    df: pd.DataFrame = st.session_state["data"]
    stats = st.session_state.get("stats")
    if stats is not None and (stats.by_rules or stats.by_ml):
        st.caption(
            f"🏷️ {stats.by_rules} categorizadas por regras · "
            f"🤖 {stats.by_ml} pela IA · ❓ {stats.uncategorized} sem categoria"
        )

    # Date filter.
    min_d, max_d = df["date"].min().date(), df["date"].max().date()
    if min_d < max_d:
        start, end = st.slider(
            "Período", min_value=min_d, max_value=max_d, value=(min_d, max_d)
        )
        mask = (df["date"].dt.date >= start) & (df["date"].dt.date <= end)
        df = df[mask]

    _render_kpis(df)
    st.divider()
    _render_charts(df)
    st.divider()
    _render_top_and_editor(df, use_ml=True)


# Streamlit executes this script with ``__name__ == "__main__"``.
if __name__ == "__main__":
    main()
