# 📉 Churn Predictor (Flask + scikit-learn)  ✅

> **Case pronto** de previsão de evasão (churn) para uma empresa de assinaturas.
> Já vem com uma **base de ~800 clientes fictícios** e um **modelo treinado
> automaticamente** — abre e usa, **sem subir CSV**. Mostra um **painel de risco**
> (quem está prestes a cancelar, receita em risco), **o que mais pesa no churn**
> e um **simulador** para pontuar um cliente hipotético.

**Skills:** Ciência de Dados / ML · Engenharia (Flask) · storytelling de dados
**Stack:** Python 3.12 · Flask · scikit-learn (RandomForest) · numpy

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** (cria o ambiente, treina e sobe) ou
`pip install -r requirements-dev.txt` + `python app.py`. Abre em
**http://localhost:5004** — e no celular pelo IP que aparece no terminal.

## ✨ O que faz
- **Painel de retenção** com KPIs: total de clientes, churn da base, **clientes
  em risco alto**, **receita em risco/mês**, ticket médio.
- **Importância das variáveis**: barras mostrando o que mais influencia o churn
  (tempo de casa, contrato, chamados ao suporte, atraso de pagamento…).
- **Qualidade do modelo**: ROC AUC e acurácia em base de teste separada.
- **Top clientes em risco**: tabela ordenada por probabilidade de cancelamento.
- **Simulador**: ajuste o perfil de um cliente e veja o **% de risco** e a
  recomendação de ação (reter / monitorar / saudável).

## 🧱 Arquitetura
```
churn-predictor/
├── app.py                 # rotas Flask (painel, simular)
├── src/churn/
│   ├── data.py            # base sintética determinística (sinal de churn realista)
│   ├── model.py           # treino (RandomForest), score, faixas de risco
│   └── service.py         # treina 1x, pontua todos, calcula KPIs
├── templates/  static/    # UI (tema analytics escuro)
└── tests/                 # dados, modelo e serviço (11 testes)
```

## 🧪 Testes
`pytest` — base determinística e com churn plausível (~0,40), o modelo aprende o
sinal (ROC AUC ~0,78), perfis de alto risco pontuam acima dos de baixo risco.

## 🗺️ Próximos
- Explicação por cliente (SHAP) e ações de retenção sugeridas por segmento.
- Exportar a lista de risco e acompanhar a evolução ao longo do tempo.
