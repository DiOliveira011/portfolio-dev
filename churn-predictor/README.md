# 🔮 Churn Predictor

> Modelo que prevê **evasão de clientes** (churn) e o serve por uma **API**,
> com explicação dos fatores de risco.

**Categoria:** Finanças/Dados · **Skills:** Ciência de Dados · Engenharia de IA (MLOps)
**Stack sugerida:** Python · scikit-learn/XGBoost · SHAP · FastAPI · Docker

## 🎯 Objetivo
Treinar um classificador de churn, avaliá-lo corretamente (validação, métricas,
matriz de confusão), explicar previsões (SHAP) e expor um endpoint que recebe um
cliente e retorna probabilidade de churn + principais fatores.

## 💼 Valor para o portfólio
Une **ciência de dados** (modelagem, avaliação, explicabilidade) com
**engenharia** (servir o modelo via API em container) — o famoso "do notebook à
produção".

## ✨ Funcionalidades (MVP)
- Pipeline de treino reprodutível (dataset → features → modelo → métricas).
- Explicabilidade com SHAP (importância global e por previsão).
- API FastAPI `/predict` + Dockerfile para subir em qualquer lugar.

## 🧱 Arquitetura
- `data`/`features`, `train` (pipeline + artefato do modelo), `serve` (FastAPI),
  `Dockerfile`, testes do contrato da API.

## 🗺️ Roadmap
- [ ] MVP: treino + métricas + API local.
- [ ] V2: Docker + CI + versionamento de modelo.
- [ ] V3: monitoramento de *data drift* e re-treino agendado.

## 📚 Dados
- Dataset público de churn (ex.: Telco) para o MVP.
