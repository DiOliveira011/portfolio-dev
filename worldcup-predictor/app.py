"""World Cup Predictor — Streamlit app. Run with: streamlit run app.py"""

from __future__ import annotations

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parent / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import plotly.express as px  # noqa: E402
import streamlit as st  # noqa: E402

from wcp.data import generate_sample_history, load_results, teams_in  # noqa: E402
from wcp.models import fit_poisson  # noqa: E402
from wcp.predict import build_elo, build_poisson, strength_ranking  # noqa: E402
from wcp.sim import simulate  # noqa: E402

st.set_page_config(page_title="World Cup Predictor", page_icon="🏆", layout="wide")
_PALETTE = px.colors.qualitative.Vivid


def _ensure_data() -> None:
    st.sidebar.title("🏆 World Cup Predictor")
    st.sidebar.caption("Previsão de jogos e título por histórico de resultados.")
    uploaded = st.sidebar.file_uploader("Histórico de jogos (CSV)", type=["csv"])
    if uploaded is not None:
        try:
            st.session_state["results"] = load_results(uploaded)
            st.sidebar.success("Histórico carregado.")
        except Exception as exc:  # noqa: BLE001
            st.sidebar.error(f"Erro ao ler CSV: {exc}")
    if st.sidebar.button("⚽ Usar histórico de exemplo", use_container_width=True):
        st.session_state["results"] = generate_sample_history()


def _render_match(results, model_name: str) -> None:
    st.subheader("🎯 Prever um jogo")
    teams = teams_in(results)
    c1, c2 = st.columns(2)
    a = c1.selectbox("Seleção A", teams, index=0)
    b = c2.selectbox("Seleção B", teams, index=1)
    if a == b:
        st.info("Escolha duas seleções diferentes.")
        return

    if model_name == "Poisson":
        _model, prob = build_poisson(results)
    else:
        _ratings, prob = build_elo(results)
    p_a, p_draw, p_b = prob(a, b)

    poisson_model = fit_poisson(results)
    score = poisson_model.most_likely_score(a, b, neutral=True)

    m1, m2, m3 = st.columns(3)
    m1.metric(f"Vitória {a}", f"{p_a * 100:.0f}%")
    m2.metric("Empate", f"{p_draw * 100:.0f}%")
    m3.metric(f"Vitória {b}", f"{p_b * 100:.0f}%")
    st.caption(f"Placar mais provável (Poisson): **{a} {score[0]} x {score[1]} {b}**")


def _render_simulation(results, prob, model_name: str) -> None:
    st.subheader("🔮 Simular o torneio")
    teams = teams_in(results)
    if len(teams) != 16:
        st.warning(
            f"A simulação usa 16 seleções (o histórico tem {len(teams)}). "
            "Use o histórico de exemplo para a demonstração completa."
        )
        return
    n_sims = st.slider("Número de simulações", 500, 8000, 2000, step=500)
    if st.button(f"Rodar {n_sims} simulações ({model_name})", type="primary"):
        with st.spinner("Simulando milhares de Copas…"):
            table = simulate(teams, prob, n_sims=n_sims, seed=7)
        fig = px.bar(
            table.head(12), x="champion", y="team", orientation="h",
            color="team", color_discrete_sequence=_PALETTE,
            title="Probabilidade de ser campeão",
        )
        fig.update_layout(showlegend=False, xaxis_tickformat=".0%", yaxis_title="")
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

        show = table.copy()
        for col in ("advance", "semifinal", "final", "champion"):
            show[col] = (show[col] * 100).map(lambda v: f"{v:.1f}%")
        st.dataframe(
            show.rename(columns={
                "team": "Seleção", "advance": "Avança do grupo",
                "semifinal": "Semifinal", "final": "Final", "champion": "Título",
            }),
            use_container_width=True, hide_index=True,
        )


def main() -> None:
    _ensure_data()
    st.title("🏆 Previsor da Copa do Mundo")

    if "results" not in st.session_state:
        st.info("👈 Clique em **Usar histórico de exemplo** ou envie um CSV de resultados.")
        with st.expander("Como funciona"):
            st.markdown(
                "- Estima a **força** de cada seleção a partir do histórico "
                "(**Elo** e **Poisson**).\n"
                "- Calcula a probabilidade de **um jogo** (vitória/empate/derrota).\n"
                "- **Simula** o torneio milhares de vezes (Monte Carlo) e mostra a "
                "chance de **título**."
            )
        return

    results = st.session_state["results"]
    model_name = st.sidebar.radio("Modelo", ["Elo", "Poisson"], horizontal=True)
    st.caption(f"{len(results)} jogos no histórico · modelo: **{model_name}**")

    st.subheader("📊 Força das seleções")
    ranking = strength_ranking(results)
    fig = px.bar(
        ranking, x="elo", y="team", orientation="h",
        color="elo", color_continuous_scale="Tealgrn", title="Rating Elo",
    )
    fig.update_layout(yaxis_title="", coloraxis_showscale=False)
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    if model_name == "Poisson":
        _m, prob = build_poisson(results)
    else:
        _r, prob = build_elo(results)

    _render_match(results, model_name)
    st.divider()
    _render_simulation(results, prob, model_name)


if __name__ == "__main__":
    main()
