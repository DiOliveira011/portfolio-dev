# 📊 Sales BI Auto-Insights (Flask)  ✅

> Um BI que **escreve os próprios achados**. Recebe uma base de vendas (já vem
> uma **fictícia carregada**, 18 meses × categoria × região × canal) e gera
> automaticamente os **"Principais achados"** em texto — tendência, melhor/pior
> mês, categoria líder, o que está **em ascensão/retração**, região destaque,
> mudança de canal e **picos de demanda** — além de KPIs e gráficos.

**Skills:** Ciência de Dados · BI / storytelling de dados · Flask
**Stack:** Python 3.12 · Flask · **só biblioteca padrão** (sem pandas/numpy)

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** ou `pip install -r requirements-dev.txt` +
`python app.py`. Abre em **http://localhost:5006**. Abre e usa — **não precisa
subir CSV**.

## ✨ O que faz
- **Achados automáticos** (motor de regras de análise): lê os dados e descreve em
  linguagem natural o que está acontecendo no negócio.
- **KPIs**: faturamento total, média mensal, **crescimento no período**,
  categoria e região líderes.
- **Gráficos** (sem dependências): faturamento por mês, por categoria, por
  região e por canal.
- **Série mensal** em tabela.

## 🧱 Arquitetura
```
sales-bi-autoinsights/
├── app.py                 # rota Flask (dashboard)
├── src/salesbi/
│   ├── data.py            # vendas sintéticas (tendência + sazonalidade)
│   └── insights.py        # agregações + motor de achados automáticos
├── templates/  static/    # UI (tema BI claro, gráficos em CSS)
└── tests/                 # dados e motor de insights (5 testes)
```

## 🧪 Testes
`pytest` — base determinística e somas consistentes, líderes corretos
(Eletrônicos / Sudeste), tendência de alta e narrativa não vazia.

## 🗺️ Próximos
- Permitir **subir um CSV** próprio (mesmo motor de insights por cima).
- Comparação período a período e export do relatório em PDF.
