# 📊 Sales BI Auto-Insights

> Jogue um **CSV de vendas** e receba um **dashboard** + **insights automáticos**
> em texto (tendências, anomalias, top produtos/clientes).

**Categoria:** Finanças/Dados · **Skills:** Ciência de Dados · (opcional) IA
**Stack sugerida:** Python · pandas · Plotly · Streamlit · (opcional) Claude para narrativa

## 🎯 Objetivo
Transformar dados brutos de vendas em um relatório executivo automático:
detecção de tipos de coluna, KPIs (faturamento, ticket médio, crescimento),
sazonalidade, e um resumo em linguagem natural dos achados.

## 💼 Valor para o portfólio
Mostra **BI/analytics de ponta a ponta** e geração de insight — exatamente o que
áreas de negócio pedem. Reaproveitável em qualquer empresa.

## ✨ Funcionalidades (MVP)
- Upload de CSV; perfil automático das colunas (datas, categóricas, numéricas).
- KPIs + gráficos (vendas no tempo, por produto/região/cliente).
- "Insights" automáticos: maiores variações, outliers, concentração (Pareto).

## 🧱 Arquitetura
- `profiling` (tipos/qualidade), `metrics` (KPIs), `insights` (regras +
  estatística; LLM opcional para texto), `dashboard` (Streamlit).

## 🗺️ Roadmap
- [ ] MVP: perfil + KPIs + gráficos + insights por regras.
- [ ] V2: narrativa por LLM e previsão de vendas.
- [ ] V3: comparação entre períodos e export PDF do relatório.

## 🔗 Relação com outros projetos
- É a "ponte" para o **doc-intelligence** (#15): mesma ideia de resumo
  automático, aqui focada em dados tabulares de vendas.
