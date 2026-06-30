# 💸 Finance Dashboard  ✅ *(MVP implementado)*

> Painel de **finanças pessoais**: importe um extrato (CSV/OFX), as transações
> são **categorizadas automaticamente** (regras + Machine Learning) e você
> visualiza para onde vai o seu dinheiro.

**Categoria:** Finanças/Dados · **Skills:** Ciência de Dados · Desenvolvimento
**Stack:** Python 3.12 · Streamlit · pandas · scikit-learn · Plotly

---

## ▶️ Como rodar

> ⚠️ **Caminho longo no Windows:** este projeto vive numa pasta do OneDrive com
> caminho muito longo. O Streamlit traz arquivos profundamente aninhados que
> estouram o limite de 260 caracteres do Windows ao instalar dentro daqui. Por
> isso a `venv` é criada **fora** do OneDrive (caminho curto). Veja
> [DECISIONS.md](../DECISIONS.md).

```bash
# venv em caminho curto (evita o limite de path do Windows)
python -m venv C:\fdv
C:\fdv\Scripts\activate
pip install -r requirements-dev.txt

# rodar o app
streamlit run app.py
```

No app: clique em **“✨ Usar dados de exemplo”** (na barra lateral) para ver tudo
funcionando na hora, ou faça **upload** do seu extrato (`.csv`/`.ofx`).

## ✨ O que faz

- **Importa** extratos em **CSV** (detecta colunas e formatos BR `1.234,56` /
  US `1,234.56`, valor único ou débito/crédito) e **OFX/QFX**.
- **Categoriza** cada transação: primeiro por **regras** (palavras-chave de
  mercados/serviços BR), depois um **classificador de texto (TF-IDF + Naive
  Bayes)** que aprende com o que as regras rotularam e preenche o resto.
- **Visualiza**: KPIs (entradas, saídas, saldo, taxa de poupança), despesas por
  categoria, fluxo mensal, saldo acumulado e maiores despesas.
- **Edita**: ajuste qualquer categoria numa tabela e tudo recalcula.

## 🧱 Arquitetura

Camadas separadas (a UI não conhece parsing nem ML diretamente):

```
finance-dashboard/
├── app.py                  # UI Streamlit (apresentação)
├── sample_data/            # extrato_exemplo.csv (gerado)
└── src/findash/
    ├── core/               # models.py, categories.py (domínio)
    ├── ingest/             # csv_parser.py, ofx_parser.py
    ├── categorize/         # rules.py + classifier.py (ML) + orquestrador
    ├── analysis/           # metrics.py (KPIs e agregações)
    ├── utils/              # formatting.py (moeda BR, normalização de texto)
    └── sample.py           # gerador de dados sintéticos (determinístico)
```

## 🧪 Testes

```bash
pytest            # 24 testes: parsing CSV/OFX, regras, pipeline de ML, métricas
ruff check .
```

## 🎨 Tema
Tema **claro com índigo/teal** e paleta de gráficos colorida (Plotly *Bold*) —
de propósito **diferente** do preto/verde do projeto Covil, para dar variedade
ao portfólio.

## 🗺️ Roadmap
- [x] MVP: importar CSV/OFX, categorizar (regras + ML), dashboard, editor.
- [ ] V2: orçamento e alertas; previsão de gasto do mês.
- [ ] V3: multi-conta, metas e exportação de relatórios (PDF).

## ⚠️ Privacidade
Roda 100% local. Nenhum dado financeiro é enviado para fora da sua máquina.
