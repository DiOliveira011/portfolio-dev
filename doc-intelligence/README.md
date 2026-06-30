# 📄 Doc Intelligence (Flask)  ✅

> Leia e **resuma qualquer documento**: cole texto ou envie **.txt, .md, .csv,
> .pdf, .xlsx**. O app extrai **estatísticas** (palavras, frases, tempo de
> leitura), **palavras-chave** e gera um **resumo** — com **IA (Groq grátis ou
> Claude)** ou um **resumo extrativo offline**. Processamento local.

**Skills:** Engenharia de IA · NLP/extração de documentos · Flask
**Stack:** Python 3.12 · Flask · pypdf · openpyxl · IA via **Groq/Claude** (urllib)

## 🤖 IA opcional (Groq grátis, Claude, ou offline)
Defina `GROQ_API_KEY` (gratuito, https://console.groq.com) **ou**
`ANTHROPIC_API_KEY` para o resumo gerado por IA. Sem chave, o app entrega um
**resumo extrativo** (as frases mais relevantes) + palavras-chave.

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** ou `pip install -r requirements-dev.txt` +
`python app.py`. Abre em **http://localhost:5009**. Clique em **"Usar exemplo"**
para testar na hora.

## ✨ O que faz
- **Lê** texto colado ou arquivos **.txt/.md/.csv/.pdf/.xlsx** (CSV/Excel também
  mostram linhas × colunas e cabeçalho).
- **Estatísticas**: palavras, frases, palavras únicas, tempo de leitura.
- **Palavras-chave** por frequência (sem stopwords).
- **Resumo**: com IA (título + resumo + pontos-chave) ou **extrativo** offline.

## 🧱 Arquitetura
```
doc-intelligence/
├── app.py                 # rota Flask (/, /analisar)
├── src/docintel/
│   ├── extract.py         # texto/CSV/PDF/Excel → texto + metadados de tabela
│   ├── analyze.py         # estatísticas, palavras-chave, resumo extrativo
│   ├── llm.py             # Groq / Claude / offline (via urllib)
│   ├── service.py         # análise + resumo (IA ou extrativo)
│   └── sample.py          # documento de exemplo
├── templates/  static/    # UI (tema documento)
└── tests/                 # extração, análise e serviço (12 testes)
```

## 🧪 Testes
`pytest` — extração de TXT/CSV (e aviso em PDF inválido), estatísticas,
palavras-chave, resumo extrativo e serviço no modo offline.

## 🗺️ Próximos
- OCR para PDFs escaneados e divisão por seções/capítulos.
- Perguntas e respostas sobre o documento (RAG por cima do texto extraído).
