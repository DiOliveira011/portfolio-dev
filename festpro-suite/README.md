# 🎉 FestPro Suite — Painel de Gestão (empresa fictícia)  ✅

> **Case de produto pronto**: o painel completo da **FestPro Eventos & Locação**,
> uma empresa **fictícia** de aluguel de itens e logística para festas/eventos.
> Já vem **cheio de dados realistas** — nada de "importe um CSV": é só abrir e
> navegar pelas telas, como um software de verdade.

**Categoria:** Produto / BI · **Skills:** Ciência de Dados · Desenvolvimento · Produto
**Stack:** Python 3.12 · Streamlit (multi-telas) · pandas · numpy · Plotly

## 🏁 Como executar (1 clique)
Dê **duplo clique em `EXECUTAR.bat`** — ele prepara o ambiente sozinho e abre no
navegador. (Ou `pip install -r requirements-dev.txt` + `streamlit run app.py`.)

## 🧭 As 6 telas
| Tela | O que mostra |
|------|--------------|
| 📊 **Visão Geral** | KPIs executivos: faturamento do mês (vs. mês anterior), eventos, ticket médio, conversão de orçamentos, NPS, entregas no prazo, ocupação de estoque, a receber + funil comercial, receita por tipo/região e backlog |
| 💰 **Vendas** | Faturamento mensal, receita por tipo, **top clientes**, ticket médio |
| 📅 **Eventos** | **Agenda** dos próximos eventos, status, eventos por mês, cancelamento |
| 📦 **Estoque** | Catálogo de itens (mesas, cadeiras, tendas…) com **% de ocupação**, manutenção e locação por categoria |
| 🚚 **Logística** | Entregas no prazo, km total e **desempenho por motorista** |
| 💵 **Financeiro** | Receita × custo × **margem** mensal, **contas a receber (aging)** e margem |

## 🧱 Como foi feito
- **`src/festpro/data.py`** — gera uma operação coerente e **determinística**:
  ~950 eventos em 13 meses (passado + agenda futura), 150 clientes (com
  recorrência tipo cauda longa), estoque e logística. Tudo embutido.
- **`src/festpro/kpis.py`** — todas as métricas/agregações (puras e testadas).
- **`app.py`** — navegação multi-telas e os gráficos.

## 🧪 Testes
`pytest` (8 testes: dataset coerente, KPIs em faixas válidas, funil monotônico).

## 🎨 Tema
Marca **FestPro** em **violeta + âmbar** — diferente das outras apps do portfólio.

> 💡 É um **case fictício** para portfólio: mostra como eu modelo o negócio,
> calculo KPIs e entrego um painel "de produto", pronto para demonstração.
