# 🧰 ML Model API Template

> Um **template de produção** para servir qualquer modelo de ML: treino
> reprodutível → API FastAPI → Docker → testes. A base de MLOps do portfólio.

**Categoria:** Engenharia de IA / MLOps · **Skills:** IA · Desenvolvimento
**Stack sugerida:** Python · scikit-learn · FastAPI · pydantic · Docker · pytest

## 🎯 Objetivo
Padronizar como modelos saem do notebook e vão para produção: estrutura de
projeto, pipeline de treino, serialização do modelo, API com validação de
entrada/saída, testes e containerização — pronto para clonar e adaptar.

## 💼 Valor para o portfólio
Mostra maturidade de **engenharia de ML** (não só treinar, mas **entregar**):
contrato de API, versionamento de artefato, testes e Docker.

## ✨ Funcionalidades (MVP)
- `train.py` reprodutível que gera um artefato versionado do modelo.
- API FastAPI com `/predict` (schema validado por pydantic) e `/health`.
- `Dockerfile` + testes do contrato da API + Makefile/CLI.

## 🧱 Arquitetura
- `training/` (pipeline + artefato), `app/` (FastAPI + schemas), `tests/`,
  `Dockerfile`. Desacoplado do modelo concreto (plugue o seu).

## 🗺️ Roadmap
- [ ] MVP: treino + API + Docker + testes.
- [ ] V2: CI (GitHub Actions), logging estruturado e métricas.
- [ ] V3: registro de modelos e *feature store* simples.

## 🔗 Sinergia
- Serve de base para colocar o **churn-predictor** (#11) em produção.
