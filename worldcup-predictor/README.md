# 🏆 World Cup Predictor  ✅ *(MVP implementado)*

> Uma "IA" que estima **probabilidades de jogos** e **chances de título** numa
> Copa do Mundo, a partir de **resultados históricos** das seleções.

> **Como rodar:** `pip install -r requirements-dev.txt` e `streamlit run app.py`.
> Clique em **“⚽ Usar histórico de exemplo”** para ver tudo funcionando. Testes: `pytest`.

**Categoria:** Dados / IA · **Skills:** Ciência de Dados · Modelagem · Simulação
**Stack sugerida:** Python · pandas · numpy · (statsmodels/scikit-learn) · Streamlit · Plotly

## 🎯 Objetivo
A partir de uma base de jogos históricos (placares de seleções), estimar a
**força de cada time** e simular o torneio milhares de vezes (Monte Carlo) para
produzir: probabilidade de cada jogo, de avançar de fase e de ser **campeão**.

## 🧠 Como prevê (abordagem)
1. **Força dos times:** dois modelos clássicos e explicáveis —
   - **Elo** (rating atualizado a cada jogo), e/ou
   - **Poisson/Dixon-Coles** (modela gols marcados/sofridos por ataque×defesa).
2. **Probabilidade de um jogo:** do modelo saem P(vitória/empate/derrota) e o
   placar mais provável.
3. **Simulação do torneio:** roda a Copa **N mil vezes** respeitando o chaveamento
   (grupos + mata-mata) e conta com que frequência cada seleção é campeã.

## 💼 Valor para o portfólio
Mostra o ciclo de DS aplicado a um tema divertido e "explicável": modelagem
estatística (Poisson/Elo), validação (acerta jogos passados?) e **simulação de
Monte Carlo** — além de visualização de probabilidades.

## ✨ Funcionalidades (MVP)
- Carregar histórico de jogos (CSV) e calcular ratings/forças por seleção.
- Prever um confronto específico (P(1/X/2) + placar provável).
- Simular o torneio e mostrar o **ranking de probabilidade de título**.
- Gráficos: força das seleções, probabilidades por fase, "favoritas".

## 🧱 Arquitetura
- `data` (carregar/limpar histórico + dataset de exemplo), `models/elo`,
  `models/poisson`, `sim` (Monte Carlo do bracket), `app` (Streamlit).

## 🗺️ Roadmap
- [ ] MVP: forças (Elo+Poisson) + previsão de jogo + simulação de campeão.
- [ ] V2: backtest (acurácia em Copas passadas) e calibração.
- [ ] V3: editor de chaveamento e cenários ("e se?").

## 📚 Dados
- Base pública de resultados de futebol internacional (ex.: "International
  football results 1872–…"). Projeto inclui um **dataset de exemplo** para rodar
  offline.

## 🎨 Tema
Paleta esportiva (verde-campo + dourado/azul) — diferente dos demais apps.

## 📝 Origem
Entra no foco no lugar de Tibia/Albion (adiados), a pedido do briefing.
