# 🗣️➡️🗃️ Text-to-SQL Analyst (Flask)  ✅

> Pergunte a um **banco de dados em português** e o app **gera o SQL, executa e
> mostra o resultado**. Vem com uma **base de vendas fictícia** já populada
> (SQLite em memória). Funciona **offline** (motor de regras) e usa **Claude**
> automaticamente se você definir `ANTHROPIC_API_KEY`. Só executa **SELECT**
> (somente leitura) — com guarda de segurança contra escrita/injeção.

**Skills:** Engenharia de IA · SQL/bancos de dados · segurança · Flask
**Stack:** Python 3.12 · Flask · sqlite3 (stdlib) · `anthropic` (opcional)

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** ou `pip install -r requirements-dev.txt` +
`python app.py`. Abre em **http://localhost:5005**. Clique numa **sugestão** ou
escreva sua pergunta.

> **Modo IA (opcional):** defina `ANTHROPIC_API_KEY` antes de abrir para liberar
> perguntas livres respondidas pelo Claude. Sem a chave, o app usa o motor de
> regras (cobre as perguntas mais comuns) — e tudo continua funcionando.

## ✨ O que faz
- **NL→SQL**: converte a pergunta em uma query SQL (Claude se houver chave; senão
  regras determinísticas para faturamento, por mês/região/categoria, top
  produtos, melhores clientes, ticket médio, contagens…).
- **Execução segura**: bloqueia qualquer coisa que não seja um único `SELECT`
  (sem `INSERT/UPDATE/DELETE/DROP/...` e sem múltiplas instruções).
- **Resultado**: mostra **o SQL gerado**, a fonte (IA/Regras) e a **tabela**.
- **Sugestões** clicáveis e **esquema do banco** à mão.

## 🧱 Arquitetura
```
text-to-sql-analyst/
├── app.py                 # rotas Flask (/, /perguntar)
├── src/t2sql/
│   ├── database.py        # SQLite em memória + seed de vendas (determinístico)
│   ├── nl2sql.py          # guarda de segurança + regras + Claude opcional
│   └── service.py         # gera, valida e executa a query
├── templates/  static/    # UI (tema escuro)
└── tests/                 # banco, NL→SQL/segurança e serviço (15 testes)
```

## 🧪 Testes
`pytest` — base determinística, mapeamento de perguntas, **bloqueio de SQL
perigoso** e execução ponta-a-ponta (offline).

## 🗺️ Próximos
- Gráfico automático para séries temporais e export CSV do resultado.
- Conectar a um banco real (Postgres) e few-shot por esquema no modo IA.
