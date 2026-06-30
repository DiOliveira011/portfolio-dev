# 📚 RAG Knowledge Assistant

> Um chatbot que **responde perguntas sobre os seus documentos** (PDF, DOCX, TXT)
> citando as fontes — Retrieval-Augmented Generation.

**Categoria:** Engenharia de IA · **Skills:** IA (LLM, embeddings, RAG)
**Stack sugerida:** Python · API da Claude · embeddings · ChromaDB/FAISS · FastAPI ou Streamlit

## 🎯 Objetivo
Indexar uma base de documentos (chunking + embeddings em um vector store) e
responder perguntas em linguagem natural, recuperando os trechos relevantes e
gerando a resposta com **citação das fontes**.

## 💼 Valor para o portfólio
RAG é uma das competências mais pedidas em IA hoje. Mostra o pipeline completo:
ingestão → chunking → embeddings → busca semântica → geração com contexto.

## ✨ Funcionalidades (MVP)
- Ingerir uma pasta de documentos e construir o índice vetorial.
- Perguntar e receber resposta fundamentada nos trechos recuperados + fontes.
- Avaliar qualidade (perguntas/respostas de teste) e evitar alucinação.

## 🧱 Arquitetura
- `ingest` (loaders + chunking), `index` (embeddings + vector store),
  `rag` (retriever + prompt + Claude), `app` (chat). Base reutilizável.

## 🗺️ Roadmap
- [ ] MVP: ingestão + busca + resposta com fontes.
- [ ] V2: histórico de conversa e filtros por documento/metadados.
- [ ] V3: avaliação automática e *re-ranking* dos trechos.

## 🔗 Base para outros projetos
- O motor de RAG aqui é reaproveitado no **ai-dungeon-master** e no
  **doc-intelligence**.

## 📚 Notas de IA
- Modelo padrão: Claude (Anthropic). Requer `ANTHROPIC_API_KEY`.
