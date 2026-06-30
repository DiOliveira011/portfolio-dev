# 📚 RAG Knowledge Assistant (Flask)  ✅

> Chatbot que responde sobre a **base de conhecimento de uma empresa fictícia**
> (Nimbus Tecnologia): RH e TI — férias, benefícios, home office, reembolso,
> segurança, onboarding, suporte. Usa **RAG**: primeiro **recupera** os trechos
> certos (TF-IDF) e depois **responde** com a IA, **citando as fontes**.

**Skills:** Engenharia de IA (RAG) · recuperação de informação · Flask
**Stack:** Python 3.12 · Flask · TF-IDF **pure-Python** · IA via **Groq/Claude**

## 🤖 IA opcional (Groq grátis, Claude, ou offline)
O app **funciona sem chave** (modo offline: mostra os trechos recuperados). Para
respostas geradas, defina **uma** variável de ambiente antes de abrir:
- `GROQ_API_KEY` — **gratuito** (https://console.groq.com), modelos Llama; ou
- `ANTHROPIC_API_KEY` — Claude.

As chamadas usam `urllib` (biblioteca padrão) — **nenhum SDK extra** é instalado.
Com as duas chaves, use `LLM_PROVIDER=groq|claude` para escolher.

## 🏁 Como executar
**Duplo clique em `EXECUTAR.bat`** ou `pip install -r requirements-dev.txt` +
`python app.py`. Abre em **http://localhost:5007**.

## ✨ O que faz
- **Recupera** (RAG) os documentos mais relevantes por similaridade TF-IDF.
- **Responde** com a IA usando *apenas* o contexto recuperado e **cita as fontes**.
- **Modo offline**: sem chave, devolve os trechos mais relevantes (busca pura).
- Mostra o **provedor ativo** (Groq / Claude / Offline) e sugestões de perguntas.

## 🧱 Arquitetura
```
rag-knowledge-assistant/
├── app.py                 # rotas Flask (/, /perguntar)
├── src/rag/
│   ├── corpus.py          # base de conhecimento (empresa fictícia)
│   ├── retriever.py       # TF-IDF + cosseno (pure-Python)
│   ├── llm.py             # Groq / Claude / offline (via urllib)
│   └── service.py         # pipeline RAG (recupera → responde)
├── templates/  static/    # UI estilo chat
└── tests/                 # retriever, provedores e serviço (11 testes)
```

## 🧪 Testes
`pytest` — recuperação relevante, resolução de provedor (sem rede) e pipeline
RAG no modo offline.

## 🗺️ Próximos
- Ingerir **seus PDFs/Markdown** e chunking por parágrafo com embeddings.
- Citar trecho exato (highlight) e histórico de conversa.
