# 🗣️➡️🗄️ Text-to-SQL Analyst

> Pergunte **em português** ("qual o faturamento por mês em 2024?") e a IA gera o
> SQL, executa no banco e responde com tabela e gráfico.

**Categoria:** Engenharia de IA · **Skills:** IA (LLM + tool use) · Ciência de Dados
**Stack sugerida:** Python · API da Claude · SQLite/DuckDB · pandas · Plotly · Streamlit

## 🎯 Objetivo
Um "analista virtual" que entende o **schema** do banco, traduz perguntas em
**SQL seguro** (somente leitura), executa e apresenta o resultado com a
visualização adequada e uma explicação.

## 💼 Valor para o portfólio
Demonstra IA aplicada a dados com **segurança** (validação de SQL, *read-only*),
*grounding* no schema real e geração de visualização — caso de uso corporativo
muito forte (self-service analytics).

## ✨ Funcionalidades (MVP)
- Conectar a um banco e ler o schema; perguntar em linguagem natural.
- Gerar SQL com a Claude, validar (apenas SELECT) e executar.
- Mostrar tabela + gráfico sugerido + explicação do que foi consultado.

## 🧱 Arquitetura
- `db` (conexão + introspecção de schema), `nl2sql` (prompt + validação),
  `viz` (escolha de gráfico), `app` (chat/console). Guardrails de segurança.

## 🗺️ Roadmap
- [ ] MVP: NL→SQL→resultado em um banco de exemplo.
- [ ] V2: memória de conversa e correção de erros de SQL automaticamente.
- [ ] V3: catálogo de métricas e cache de consultas frequentes.

## 📚 Notas de IA
- Modelo padrão: Claude (Anthropic). SQL sempre validado antes de executar.
