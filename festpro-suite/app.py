"""FestPro Suite — painel completo de uma empresa fictícia de eventos & locação.

Run: streamlit run app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import plotly.express as px  # noqa: E402
import streamlit as st  # noqa: E402

from festpro import COMPANY_NAME, kpis  # noqa: E402
from festpro import data as fdata  # noqa: E402

st.set_page_config(page_title="FestPro Suite", page_icon="🎉", layout="wide")
_PALETTE = px.colors.qualitative.Bold


@st.cache_data
def _load() -> fdata.CompanyData:
    return fdata.generate_company_data()


def brl(value: float) -> str:
    return f"R$ {value:,.0f}".replace(",", ".")


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
def page_overview(data: fdata.CompanyData) -> None:
    st.subheader("📊 Visão Geral")
    o = kpis.overview(data)
    delta = f"{o.revenue_delta * 100:.0f}% vs mês ant."
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Faturamento (mês)", brl(o.revenue_month), delta)
    c2.metric("Eventos (mês)", o.events_month)
    c3.metric("Ticket médio", brl(o.avg_ticket))
    c4.metric("Conversão de orçamentos", f"{o.conversion * 100:.0f}%")
    c5, c6, c7, c8 = st.columns(4)
    c5.metric("NPS", f"{o.nps:.1f}")
    c6.metric("Entregas no prazo", f"{o.on_time * 100:.0f}%")
    c7.metric("Ocupação do estoque", f"{o.inventory_util * 100:.0f}%")
    c8.metric("A receber", brl(o.receivables))

    left, right = st.columns([3, 2])
    with left:
        rev = kpis.revenue_by_month(data.events)
        fig = px.area(rev, x="month", y="revenue", title="Faturamento mensal (realizado)",
                      color_discrete_sequence=["#7c3aed"])
        fig.update_layout(xaxis_title="", yaxis_title="R$")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        types = kpis.by_type(data.events)
        fig2 = px.pie(types, names="type", values="receita", title="Receita por tipo de evento",
                      color_discrete_sequence=_PALETTE, hole=0.45)
        st.plotly_chart(fig2, use_container_width=True)

    a, b = st.columns(2)
    with a:
        fun = kpis.funnel(data.events, data.as_of)
        fig3 = px.funnel(fun, x="quantidade", y="etapa", title="Funil comercial",
                         color_discrete_sequence=["#7c3aed"])
        st.plotly_chart(fig3, use_container_width=True)
    with b:
        reg = kpis.by_region(data.events)
        fig4 = px.bar(reg, x="revenue", y="region", orientation="h", title="Receita por região",
                      color="region", color_discrete_sequence=_PALETTE)
        fig4.update_layout(showlegend=False, xaxis_title="R$", yaxis_title="")
        st.plotly_chart(fig4, use_container_width=True)
    st.caption(f"Carteira futura confirmada (backlog): **{brl(o.backlog)}**")


def page_sales(data: fdata.CompanyData) -> None:
    st.subheader("💰 Vendas & Orçamentos")
    real = kpis.realized(data.events)
    c1, c2, c3 = st.columns(3)
    c1.metric("Receita realizada (total)", brl(real["revenue"].sum()))
    c2.metric("Ticket médio", brl(real["revenue"].mean() if len(real) else 0))
    c3.metric("Eventos realizados", len(real))

    rev = kpis.revenue_by_month(data.events)
    fig = px.bar(rev, x="month", y="revenue", title="Faturamento mensal",
                 color_discrete_sequence=["#7c3aed"])
    fig.update_layout(xaxis_title="", yaxis_title="R$")
    st.plotly_chart(fig, use_container_width=True)

    a, b = st.columns(2)
    with a:
        types = kpis.by_type(data.events)
        st.plotly_chart(
            px.bar(types, x="receita", y="type", orientation="h", title="Receita por tipo",
                   color="type", color_discrete_sequence=_PALETTE).update_layout(showlegend=False),
            use_container_width=True,
        )
    with b:
        st.markdown("**Top clientes**")
        top = kpis.top_clients(data.events)
        top["receita"] = top["receita"].map(brl)
        st.dataframe(top.rename(columns={
            "client": "Cliente", "segment": "Segmento", "eventos": "Eventos", "receita": "Receita",
        }), use_container_width=True, hide_index=True)


def page_events(data: fdata.CompanyData) -> None:
    st.subheader("📅 Eventos & Agenda")
    ev, as_of = data.events, data.as_of
    realized = (ev["status"] == "Realizado").sum()
    confirmed_future = ((ev["status"] == "Confirmado") & (ev["date"] > as_of)).sum()
    open_quotes = ((ev["status"] == "Orçamento") & (ev["date"] > as_of)).sum()
    cancel_rate = (kpis.past(ev, as_of)["status"] == "Cancelado").mean()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Realizados", int(realized))
    c2.metric("Confirmados (futuros)", int(confirmed_future))
    c3.metric("Orçamentos abertos", int(open_quotes))
    c4.metric("Taxa de cancelamento", f"{cancel_rate * 100:.0f}%")

    st.markdown("**Próximos eventos**")
    up = kpis.upcoming_events(ev, as_of)
    up["date"] = up["date"].dt.strftime("%d/%m/%Y")
    up["revenue"] = up["revenue"].map(brl)
    st.dataframe(up.rename(columns={
        "date": "Data", "client": "Cliente", "type": "Tipo", "region": "Região",
        "guests": "Convidados", "revenue": "Valor", "status": "Status",
    }), use_container_width=True, hide_index=True)

    a, b = st.columns(2)
    with a:
        counts = ev["status"].value_counts().reset_index()
        counts.columns = ["status", "qtd"]
        st.plotly_chart(
            px.pie(counts, names="status", values="qtd", title="Eventos por status",
                   color_discrete_sequence=_PALETTE, hole=0.4),
            use_container_width=True,
        )
    with b:
        monthly = ev.assign(month=ev["date"].dt.to_period("M").astype(str))
        per = monthly.groupby("month", as_index=False)["event_id"].count().tail(12)
        st.plotly_chart(
            px.bar(per, x="month", y="event_id", title="Eventos por mês",
                   color_discrete_sequence=["#7c3aed"]).update_layout(
                       xaxis_title="", yaxis_title="eventos"),
            use_container_width=True,
        )


def page_inventory(data: fdata.CompanyData) -> None:
    st.subheader("📦 Estoque & Locação")
    inv = data.inventory.assign(util_pct=lambda d: d["utilization"] * 100)
    c1, c2, c3 = st.columns(3)
    c1.metric("Ocupação média", f"{inv['utilization'].mean() * 100:.0f}%")
    c2.metric("Itens locados", int(inv["rented"].sum()))
    c3.metric("Em manutenção", int(inv["maintenance"].sum()))

    st.dataframe(
        inv[["item", "category", "total", "rented", "available", "maintenance", "util_pct"]]
        .rename(columns={
            "item": "Item", "category": "Categoria", "total": "Total", "rented": "Locado",
            "available": "Disponível", "maintenance": "Manutenção", "util_pct": "Ocupação",
        }),
        use_container_width=True, hide_index=True,
        column_config={
            "Ocupação": st.column_config.ProgressColumn(
                "Ocupação", min_value=0, max_value=100, format="%.0f%%"),
        },
    )
    a, b = st.columns(2)
    with a:
        st.plotly_chart(
            px.bar(inv.sort_values("utilization"), x="utilization", y="item", orientation="h",
                   title="Ocupação por item", color="utilization",
                   color_continuous_scale="Purples").update_layout(
                       coloraxis_showscale=False, xaxis_tickformat=".0%", yaxis_title=""),
            use_container_width=True,
        )
    with b:
        cat = inv.groupby("category", as_index=False)["rented"].sum()
        st.plotly_chart(
            px.pie(cat, names="category", values="rented", title="Itens locados por categoria",
                   color_discrete_sequence=_PALETTE, hole=0.4),
            use_container_width=True,
        )


def page_logistics(data: fdata.CompanyData) -> None:
    st.subheader("🚚 Logística")
    real = kpis.realized(data.events)
    c1, c2, c3 = st.columns(3)
    c1.metric("Entregas realizadas", len(real))
    c2.metric("No prazo", f"{real['on_time'].dropna().mean() * 100:.0f}%")
    c3.metric("Km total", f"{real['delivery_km'].sum():,.0f} km".replace(",", "."))

    drv = kpis.deliveries_by_driver(data.events)
    a, b = st.columns(2)
    with a:
        st.plotly_chart(
            px.bar(drv, x="km", y="driver", orientation="h", title="Km por motorista",
                   color="driver", color_discrete_sequence=_PALETTE).update_layout(
                       showlegend=False, yaxis_title=""),
            use_container_width=True,
        )
    with b:
        show = drv.copy()
        show["no_prazo"] = (show["no_prazo"] * 100).map(lambda v: f"{v:.0f}%")
        show["km"] = show["km"].map(lambda v: f"{v:,.0f}".replace(",", "."))
        st.markdown("**Desempenho por motorista**")
        st.dataframe(show.rename(columns={
            "driver": "Motorista", "entregas": "Entregas", "km": "Km", "no_prazo": "No prazo",
        }), use_container_width=True, hide_index=True)


def page_finance(data: fdata.CompanyData) -> None:
    st.subheader("💵 Financeiro")
    fin = kpis.finance_monthly(data.events)
    rev, cost, margin = fin["revenue"].sum(), fin["cost"].sum(), fin["margin"].sum()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Receita (12m)", brl(rev))
    c2.metric("Custo (12m)", brl(cost))
    c3.metric("Margem (12m)", brl(margin))
    c4.metric("Margem %", f"{(margin / rev * 100) if rev else 0:.0f}%")

    melted = fin.melt(id_vars="month", value_vars=["revenue", "cost"],
                      var_name="tipo", value_name="valor").replace(
        {"revenue": "Receita", "cost": "Custo"})
    fig = px.bar(melted, x="month", y="valor", color="tipo", barmode="group",
                 title="Receita vs custo", color_discrete_sequence=["#7c3aed", "#f59e0b"])
    fig.update_layout(xaxis_title="", yaxis_title="R$", legend_title="")
    st.plotly_chart(fig, use_container_width=True)

    a, b = st.columns(2)
    with a:
        aging = kpis.receivables_aging(data.events, data.as_of)
        st.plotly_chart(
            px.bar(aging, x="faixa", y="valor", title="Contas a receber (aging)",
                   color="faixa", color_discrete_sequence=_PALETTE).update_layout(
                       showlegend=False, xaxis_title="", yaxis_title="R$"),
            use_container_width=True,
        )
    with b:
        st.plotly_chart(
            px.line(fin, x="month", y="margin", title="Margem mensal",
                    color_discrete_sequence=["#16a34a"], markers=True).update_layout(
                        xaxis_title="", yaxis_title="R$"),
            use_container_width=True,
        )


_PAGES = {
    "📊 Visão Geral": page_overview,
    "💰 Vendas": page_sales,
    "📅 Eventos": page_events,
    "📦 Estoque": page_inventory,
    "🚚 Logística": page_logistics,
    "💵 Financeiro": page_finance,
}


def main() -> None:
    data = _load()
    st.sidebar.title("🎉 FestPro")
    st.sidebar.caption(COMPANY_NAME)
    choice = st.sidebar.radio("Navegação", list(_PAGES), label_visibility="collapsed")
    st.sidebar.divider()
    st.sidebar.metric("Eventos na base", len(data.events))
    st.sidebar.caption(f"Dados de demonstração · base em {data.as_of:%d/%m/%Y}")

    st.title("FestPro Suite")
    st.caption("Painel de gestão — empresa fictícia de eventos & locação")
    _PAGES[choice](data)


if __name__ == "__main__":
    main()
