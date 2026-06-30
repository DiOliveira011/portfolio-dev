# 💹 Albion Profit Engine

> Calculadora de **lucro de crafting** e **arbitragem entre cidades** do
> **Albion Online**, usando os preços de mercado da comunidade.

**Categoria:** Mundo Nerd / MMO · **Skills:** Ciência de Dados · Desenvolvimento
**Stack sugerida:** Python · Albion Online Data Project API · pandas · Streamlit/CustomTkinter

## 🎯 Objetivo
Responder de forma prática "o que vale a pena craftar/transportar agora?":
puxar preços por cidade/qualidade, descontar taxas e *return rate*, e ranquear
oportunidades de lucro.

## 💼 Valor para o portfólio
Caso clássico de **decisão orientada a dados** com impacto direto — modelagem de
custos, joins entre receitas e preços, e um produto que "dá dinheiro" no jogo.

## ✨ Funcionalidades (MVP)
- Buscar preços atuais por item/cidade/qualidade (Albion Data Project API).
- Calcular lucro de crafting (insumos × preço, taxas, foco/return rate).
- Detectar arbitragem: comprar barato numa cidade, vender caro em outra.

## 🧱 Arquitetura
- `services/albion` (cliente + cache), `domain` (receitas/itens), `engine`
  (cálculo de lucro/arbitragem), `ui` (tabelas ranqueadas e filtros).

## 🗺️ Roadmap
- [ ] MVP: preços + lucro de crafting + ranking.
- [ ] V2: arbitragem entre cidades com custo de transporte/risco.
- [ ] V3: histórico de preços e alertas de oportunidade.

## 📚 Dados / APIs
- Albion Online Data Project (preços de mercado crowdsourced).
