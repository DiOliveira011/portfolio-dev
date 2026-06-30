"""Logistics Control — Streamlit app (B2B distribution). Run: streamlit run app.py"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import pandas as pd  # noqa: E402
import plotly.express as px  # noqa: E402
import streamlit as st  # noqa: E402

from logistics.core import Delivery, hhmm_to_minutes, minutes_to_hhmm  # noqa: E402
from logistics.fleet import generate_history, summarize_drivers  # noqa: E402
from logistics.routing import plan, summarize  # noqa: E402
from logistics.sample import (  # noqa: E402
    sample_deliveries,
    sample_depot,
    sample_drivers,
    sample_vehicles,
)

st.set_page_config(page_title="Logistics Control", page_icon="🚚", layout="wide")
_PALETTE = px.colors.qualitative.Set1


def _ensure_state() -> None:
    if "deliveries" not in st.session_state:
        st.session_state["deliveries"] = sample_deliveries()
        st.session_state["vehicles"] = sample_vehicles()
        st.session_state["drivers"] = sample_drivers()
        st.session_state["depot"] = sample_depot()
        st.session_state["fuel_price"] = 6.00


def _sidebar() -> None:
    st.sidebar.title("🚚 Logistics Control")
    st.sidebar.caption("Distribuição B2B: rotas, motoristas, combustível e baixa.")
    depot = st.session_state["depot"]
    depot.start_min = st.sidebar.slider("Início da operação", 5, 12, depot.start_min // 60) * 60
    st.session_state["fuel_price"] = st.sidebar.number_input(
        "Preço do combustível (R$/L)", 1.0, 15.0, st.session_state["fuel_price"], step=0.1
    )
    if st.sidebar.button("♻️ Restaurar exemplo", use_container_width=True):
        for key in ("deliveries", "vehicles", "drivers", "history"):
            st.session_state.pop(key, None)
        _ensure_state()

    with st.sidebar.expander("➕ Nova entrega"), st.form("nova_entrega", clear_on_submit=True):
        label = st.text_input("Cliente / empresa", "Novo cliente")
        lat = st.number_input("Latitude", value=-23.55, format="%.4f")
        lon = st.number_input("Longitude", value=-46.63, format="%.4f")
        vol = st.number_input("Volume", 1.0, 50.0, 3.0)
        ws = st.text_input("Janela início (HH:MM)", "09:00")
        we = st.text_input("Janela fim (HH:MM)", "12:00")
        items = st.text_input("Mercadorias (vírgula)", "Mesas, Cadeiras")
        kind = st.selectbox("Tipo", ["entrega", "retirada"])
        if st.form_submit_button("Adicionar"):
            ds = st.session_state["deliveries"]
            ds.append(Delivery(
                id=f"D{len(ds) + 1:02d}", label=label, lat=lat, lon=lon, volume=vol,
                window_start=hhmm_to_minutes(ws), window_end=hhmm_to_minutes(we),
                kind=kind, items=[i.strip() for i in items.split(",") if i.strip()],
            ))


def _driver_lookup() -> dict[str, object]:
    return {d.id: d for d in st.session_state["drivers"]}


def _janela(delivery) -> str:
    return f"{minutes_to_hhmm(delivery.window_start)}–{minutes_to_hhmm(delivery.window_end)}"


def _render_map(routes, depot) -> None:
    rows: list[dict[str, object]] = []
    for route in routes:
        if not route.stops:
            continue
        rows.append({"vehicle": route.vehicle.name, "order": 0,
                     "lat": depot.lat, "lon": depot.lon, "label": "Base"})
        for order, stop in enumerate(route.stops, start=1):
            rows.append({"vehicle": route.vehicle.name, "order": order,
                         "lat": stop.delivery.lat, "lon": stop.delivery.lon,
                         "label": stop.delivery.label})
    if not rows:
        st.info("Nenhuma rota para exibir.")
        return
    df = pd.DataFrame(rows).sort_values(["vehicle", "order"])
    fig = px.line_mapbox(df, lat="lat", lon="lon", color="vehicle", hover_name="label",
                         color_discrete_sequence=_PALETTE, zoom=9, height=480)
    fig.update_traces(mode="lines+markers")
    fig.add_scattermapbox(lat=[depot.lat], lon=[depot.lon], mode="markers+text",
                          text=["BASE"], textposition="top center",
                          marker={"size": 16, "color": "#0f172a"}, name="Base")
    fig.update_layout(mapbox_style="open-street-map", margin={"l": 0, "r": 0, "t": 0, "b": 0})
    st.plotly_chart(fig, use_container_width=True)


def _tab_planning() -> None:
    deliveries = st.session_state["deliveries"]
    vehicles = st.session_state["vehicles"]
    depot = st.session_state["depot"]
    price = st.session_state["fuel_price"]
    drivers = _driver_lookup()

    routes, unassigned = plan(deliveries, vehicles, depot)
    kpis = summarize(routes, unassigned)
    fuel_total = sum(r.fuel_cost(price) for r in routes)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Entregas", int(kpis["deliveries"]))
    c2.metric("No prazo", f"{kpis['on_time_pct'] * 100:.0f}%")
    c3.metric("Km total", f"{kpis['total_km']:.0f} km")
    c4.metric("Combustível", f"R$ {fuel_total:.0f}")
    c5.metric("Sem atribuição", int(kpis["unassigned"]))

    if unassigned:
        st.warning("Sem capacidade para: " + ", ".join(d.label for d in unassigned))

    st.subheader("🗺️ Mapa das rotas")
    _render_map(routes, depot)

    st.subheader("🧾 Rotas e romaneio por veículo")
    for route in routes:
        if not route.stops:
            continue
        drv = drivers.get(route.vehicle.driver_id)
        drv_txt = f"{drv.name} · {drv.phone}" if drv else "sem motorista"
        header = (
            f"{route.vehicle.name} ({route.vehicle.plate}) — {drv_txt} · "
            f"{len(route.stops)} paradas · {route.total_km:.0f} km · "
            f"⛽ {route.fuel_liters:.0f} L (R$ {route.fuel_cost(price):.0f}) · "
            f"{route.on_time_count}/{len(route.stops)} no prazo"
        )
        with st.expander(header):
            data = [{
                "#": i, "Cliente": s.delivery.label,
                "Mercadorias": ", ".join(s.delivery.items) or "—",
                "Janela": _janela(s.delivery),
                "Sair às": minutes_to_hhmm(depot.start_min) if i == 1 else "",
                "Chegada": minutes_to_hhmm(s.arrival_min),
                "No prazo": "✅" if s.on_time else "⛔",
            } for i, s in enumerate(route.stops, start=1)]
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

    _render_manifest(routes)


def _render_manifest(routes) -> None:
    st.subheader("✍️ Manifesto & baixa (conferente)")
    rows = [{
        "id": s.delivery.id, "Veículo": r.vehicle.name, "Cliente": s.delivery.label,
        "Mercadorias": ", ".join(s.delivery.items) or "—",
        "Conferente": s.delivery.receiver or "", "Status": s.delivery.status,
    } for r in routes for s in r.stops]
    if not rows:
        return
    edited = st.data_editor(
        pd.DataFrame(rows), use_container_width=True, hide_index=True, key="manifest",
        column_config={
            "id": None,
            "Veículo": st.column_config.TextColumn(disabled=True),
            "Cliente": st.column_config.TextColumn(disabled=True),
            "Mercadorias": st.column_config.TextColumn(disabled=True),
            "Conferente": st.column_config.TextColumn("Conferente (quem recebeu)"),
            "Status": st.column_config.SelectboxColumn(
                options=["pendente", "entregue", "recusado"]),
        },
    )
    by_id = {d.id: d for d in st.session_state["deliveries"]}
    changed = False
    for row in edited.to_dict("records"):
        d = by_id.get(row["id"])
        if d and (d.receiver != (row["Conferente"] or None) or d.status != row["Status"]):
            d.receiver = row["Conferente"] or None
            d.status = row["Status"]
            changed = True
    if changed:
        st.toast("Baixa atualizada.")


def _tab_fleet() -> None:
    drivers = st.session_state["drivers"]
    vehicles = st.session_state["vehicles"]
    if "history" not in st.session_state:
        st.session_state["history"] = generate_history(drivers, vehicles)
    history = st.session_state["history"]
    report = summarize_drivers(history)
    phones = {d.id: d.phone for d in drivers}
    report = report.assign(telefone=report["driver_id"].map(phones))

    f1, f2, f3 = st.columns(3)
    f1.metric("Km no mês (frota)", f"{report['km_mes'].sum():.0f} km")
    f2.metric("Combustível no mês", f"R$ {report['combustivel_mes'].sum():.0f}")
    f3.metric("Entregas no mês", int(report["entregas_mes"].sum()))

    st.subheader("🧑‍✈️ Motoristas")
    view = report[["driver", "telefone", "km_dia", "km_semana", "km_mes",
                   "combustivel_mes", "entregas_mes"]].rename(columns={
        "driver": "Motorista", "telefone": "Telefone", "km_dia": "Km dia",
        "km_semana": "Km semana", "km_mes": "Km mês",
        "combustivel_mes": "Combustível mês (R$)", "entregas_mes": "Entregas mês",
    })
    st.dataframe(view, use_container_width=True, hide_index=True)

    g1, g2 = st.columns(2)
    with g1:
        st.caption("Km no mês por motorista")
        fig = px.bar(report, x="km_mes", y="driver", orientation="h",
                     color="driver", color_discrete_sequence=_PALETTE)
        fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="km")
        st.plotly_chart(fig, use_container_width=True)
    with g2:
        st.caption("Custo de combustível por dia (frota)")
        daily = history.groupby("date", as_index=False)["fuel_cost"].sum()
        fig2 = px.line(daily, x="date", y="fuel_cost", color_discrete_sequence=["#f59e0b"])
        fig2.update_layout(xaxis_title="", yaxis_title="R$")
        st.plotly_chart(fig2, use_container_width=True)


def main() -> None:
    _ensure_state()
    _sidebar()
    st.title("🚚 Controle de Logística — Distribuição B2B")
    tab1, tab2 = st.tabs(["🗺️ Planejamento do dia", "🧑‍✈️ Motoristas & Frota"])
    with tab1:
        _tab_planning()
    with tab2:
        _tab_fleet()


if __name__ == "__main__":
    main()
