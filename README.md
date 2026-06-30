<div align="center">

# 🚀 Projetos — Grupo Desenvolvimento

**Portfólio de Desenvolvimento de Software, Ciência de Dados e Engenharia de IA.**

Do mundo nerd (Magic Commander, D&D, Daggerheart, Old Dragon) ao mundo
financeiro, de dados e empresarial — cada projeto demonstra competências reais e
tem valor de negócio.

![status](https://img.shields.io/badge/status-em%20construção-4f46e5)
![python](https://img.shields.io/badge/python-3.12%2B-3776AB)
![foco](https://img.shields.io/badge/foco-Dev%20%7C%20Data%20%7C%20IA-6f42c1)

</div>

---

## 🎯 Objetivo

Reunir, **organizado em pastas**, aplicações e soluções que mostram domínio de
**Desenvolvimento**, **Ciência de Dados** e **Engenharia de IA**. Cada pasta é um
projeto independente, com `README` próprio e — conforme implementamos — código,
testes e instruções. Cada app usa uma **paleta de cores diferente** (variedade).

> 📌 Decisões de projeto registradas em **[DECISIONS.md](./DECISIONS.md)**.

## ▶️ Como executar (1 clique)

Os apps já implementados rodam com **duplo clique**: entre na pasta do app e
execute **`EXECUTAR.bat`**. Na primeira vez ele cria o ambiente Python sozinho
(num caminho curto, fora do OneDrive — por causa do limite de caminho do Windows)
e abre o app no navegador. Para abrir os quatro de uma vez, use o
**`INICIAR-TUDO.bat`** na raiz.

> Requisito único: ter o **Python 3.12+** instalado
> ([python.org/downloads](https://www.python.org/downloads/), marque
> *"Add Python to PATH"*).

## 📦 Projetos

### 🎲 Mundo Nerd / Games
| # | Projeto | O que é | Skills |
|---|---------|---------|--------|
| 1 | [mtg-deck-lab](./mtg-deck-lab) ✅ | Analisador **Commander** (Flask): cole lista/link, brackets (1–5), curva, preço + **câmera no celular** | Dev |
| 2 | [mtg-card-vision](./mtg-card-vision) | Reconhece cartas por foto (visão computacional) | IA |
| 3 | [rpg-character-forge](./rpg-character-forge) ✅ | **(Flask)** fichas D&D 5e (forjar/aleatório, imprimível) | Dev |
| 4 | [ai-dungeon-master](./ai-dungeon-master) | Mestre de RPG com IA + memória de campanha | IA |

### ⚽ Esportes / Dados
| # | Projeto | O que é | Skills |
|---|---------|---------|--------|
| 5 | [worldcup-predictor](./worldcup-predictor) ✅ | Prevê jogos e campeão da Copa por histórico (Elo/Poisson + Monte Carlo) | Data · IA |

### 💰 Finanças / Dados
| # | Projeto | O que é | Skills |
|---|---------|---------|--------|
| 6 | [finance-dashboard](./finance-dashboard) ✅ | Dashboard de finanças com categorização por ML | Data · Dev |
| 7 | [invest-portfolio-analyzer](./invest-portfolio-analyzer) ✅ | Risco/retorno + fronteira eficiente (Monte Carlo) | Data |
| 8 | [nfe-invoice-extractor](./nfe-invoice-extractor) ✅ | **(Flask)** extrai e valida NF-e (XML) + export CSV | Dev |
| 9 | [sales-bi-autoinsights](./sales-bi-autoinsights) | CSV de vendas → dashboard + insights | Data |
| 10 | [churn-predictor](./churn-predictor) | Prevê evasão de clientes + API (MLOps) | Data · IA |

### 🚚 Empresarial / Logística
| # | Projeto | O que é | Skills |
|---|---------|---------|--------|
| 11 | [logistics-control](./logistics-control) ✅ | Planejamento de rotas/frota + BI (Streamlit) | Dev · Data |
| 11b | [gestao-entregas](./gestao-entregas) ✅ | **(Flask)** gestão operacional: cadastro, **baixa c/ conferente**, SLA com feriados, auditoria | Dev |

### 🤖 Engenharia de IA
| # | Projeto | O que é | Skills |
|---|---------|---------|--------|
| 12 | [rag-knowledge-assistant](./rag-knowledge-assistant) | Chatbot sobre seus documentos (RAG) | IA |
| 13 | [text-to-sql-analyst](./text-to-sql-analyst) | Pergunte em PT, ele consulta o banco | IA · Data |
| 14 | [ml-model-api-template](./ml-model-api-template) ✅ | **(FastAPI)** modelo + `/predict` + Docker (base MLOps) | IA · Dev |
| 15 | [doc-intelligence](./doc-intelligence) | **(por último)** Lê PDF/Excel e resume com IA | IA · Data |

### 🧊 Backlog (depois)
| Projeto | O que é |
|---------|---------|
| [tibia-market-radar](./tibia-market-radar) | Dados/mercado do Tibia (adiado a pedido) |
| [albion-profit-engine](./albion-profit-engine) | Lucro/arbitragem no Albion (adiado a pedido) |

## ⭐ Destaque — [festpro-suite](./festpro-suite)
**Case de "produto pronto"**: o painel de gestão completo de uma **empresa
fictícia de eventos & locação** (FestPro), já cheio de dados realistas e com
**6 telas** (Visão Geral, Vendas, Eventos, Estoque, Logística, Financeiro) e
dezenas de KPIs. **Não é "importe um CSV"** — abre e usa, como software de verdade.

## ✅ Progresso
**10 apps implementados e verificados** (lint + testes + boot):
- 🃏 `mtg-deck-lab` — **(Flask)** analisador de Commander: lista/link, brackets,
  curva, preço, **câmera no celular**.
- 🤖 `ml-model-api-template` — **(FastAPI)** treina e serve um modelo (/predict,
  /docs Swagger, Docker) — base de MLOps reutilizável.
- 🧾 `nfe-invoice-extractor` — **(Flask)** lê NF-e (XML), valida e exporta itens em CSV.
- ⚔️ `rpg-character-forge` — **(Flask)** fichas de D&D 5e (forjar/aleatório, imprimível).
- 🚚 `gestao-entregas` — **(Flask)** gestão operacional de entregas (cadastro,
  baixa com conferente, SLA com feriados, auditoria).
- ⭐ `festpro-suite` — painel completo de empresa fictícia (6 telas, KPIs, BI).
- ✅ `finance-dashboard` — importa extrato, categoriza com regras+ML, dashboard.
- ✅ `worldcup-predictor` — Elo/Poisson + simulação de Monte Carlo do torneio.
- ✅ `logistics-control` — distribuição B2B: rotas, motorista, combustível, baixa.
- ✅ `invest-portfolio-analyzer` — risco/retorno + fronteira eficiente.



## 🛠️ Convenções
- **Python 3.12+**, código tipado, testes e `README` por projeto.
- IA: modelo padrão **Claude (Anthropic)** quando há LLM.
- **GitHub:** por enquanto tudo **local**; subimos para
  `Projetos-Grupo-Desenvolvimento` quando aprovado.
