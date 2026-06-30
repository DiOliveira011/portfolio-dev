# 🛡️ Tibia Market Radar

> Coleta dados públicos do **Tibia** (mercado, personagens, bosses, mundos) e
> transforma em dashboards e previsões.

**Categoria:** Mundo Nerd / MMO · **Skills:** Ciência de Dados (ETL, séries temporais)
**Stack sugerida:** Python · TibiaData API · pandas · SQLite · Streamlit/Plotly · (opcional) Prophet

## 🎯 Objetivo
Montar um pipeline que coleta periodicamente dados da
[TibiaData API](https://tibiadata.com/) e gera análises: tracking de bosses,
status de mundos, e tendências de itens/preços ao longo do tempo.

## 💼 Valor para o portfólio
Demonstra **engenharia de dados leve** (coleta agendada, armazenamento,
limpeza) + análise temporal + visualização — o ciclo completo de DS.

## ✨ Funcionalidades (MVP)
- Coletor agendado que salva snapshots em SQLite.
- Dashboard: mundos online, chance/tracking de bosses, ranking de personagens.
- Série temporal de um indicador escolhido com tendência.

## 🧱 Arquitetura
- `collector` (jobs + cliente da API), `storage` (SQLite/parquet),
  `analysis` (pandas), `dashboard` (Streamlit/Plotly).

## 🗺️ Roadmap
- [ ] MVP: coletor + dashboard básico.
- [ ] V2: previsão de séries (preços/atividade) e alertas.
- [ ] V3: histórico longo + comparações entre mundos.

## 📚 Dados / APIs
- TibiaData API (dados oficiais agregados do Tibia).
