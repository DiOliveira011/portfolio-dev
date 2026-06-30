# 📈 Invest Portfolio Analyzer  ✅ *(MVP implementado)*

> Análise de **carteira de investimentos**: risco, retorno, correlações e uma
> **fronteira eficiente** por Monte Carlo (carteira de máximo Sharpe).

> **Como rodar:** `pip install -r requirements-dev.txt` e `streamlit run app.py`.
> Roda **offline** com preços sintéticos (GBM); para preços reais,
> `pip install yfinance` e escolha “Buscar (yfinance)”. Testes: `pytest`.

**Categoria:** Finanças/Dados · **Skills:** Ciência de Dados (quant)
**Stack sugerida:** Python · yfinance · pandas · numpy · Plotly · Streamlit

## 🎯 Objetivo
Receber a composição da carteira e calcular métricas de risco/retorno
(volatilidade, Sharpe, *drawdown*), correlação entre ativos e comparar com um
benchmark — além de um *backtest* básico.

## 💼 Valor para o portfólio
Demonstra finanças quantitativas: manipulação de séries de preços, métricas de
risco e visualização — muito valorizado em vagas de dados no mercado financeiro.

## ✨ Funcionalidades (MVP)
- Inserir ativos e pesos; baixar histórico (yfinance).
- Métricas: retorno acumulado, volatilidade, Sharpe, *max drawdown*.
- Matriz de correlação e comparação com benchmark (ex.: IBOV/S&P500).

## 🧱 Arquitetura
- `data` (preços + cache), `metrics` (risco/retorno), `backtest`,
  `dashboard` (Plotly/Streamlit).

## 🗺️ Roadmap
- [ ] MVP: métricas + correlação + comparação com índice.
- [ ] V2: otimização de carteira (fronteira eficiente de Markowitz).
- [ ] V3: rebalanceamento e relatórios periódicos.

## ⚠️ Aviso
- Ferramenta educacional — não é recomendação de investimento.
