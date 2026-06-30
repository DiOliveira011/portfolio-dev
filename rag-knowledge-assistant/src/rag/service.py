"""RAG service: retrieve context, then answer with the LLM (or offline fallback)."""

from __future__ import annotations

from rag import llm
from rag.corpus import COMPANY, DOCS
from rag.retriever import Retriever

_SYSTEM = (
    f"Você é o assistente interno de RH e TI da empresa {COMPANY}. "
    "Responda à pergunta do colaborador em português, de forma objetiva e cordial, "
    "USANDO APENAS o CONTEXTO fornecido. Se a resposta não estiver no contexto, "
    "diga que não encontrou essa informação. Ao final, cite entre parênteses as "
    "seções usadas."
)


class RagService:
    def __init__(self) -> None:
        self.retriever = Retriever(DOCS)

    def ask(self, question: str, k: int = 3) -> dict:
        question = (question or "").strip()
        if not question:
            return {"answer": "Digite uma pergunta.", "sources": [],
                    "provider": llm.provider_label(), "mode": "vazio"}

        hits = self.retriever.retrieve(question, k=k)
        if not hits:
            return {"answer": "Não encontrei nada relacionado na base de conhecimento. "
                    "Tente reformular a pergunta.", "sources": [],
                    "provider": llm.provider_label(), "mode": "offline"}

        context = "\n\n".join(f"[{h['title']}]\n{h['text']}" for h in hits)

        if llm.available():
            user = f"CONTEXTO:\n{context}\n\nPERGUNTA: {question}"
            answer = llm.complete(_SYSTEM, user, max_tokens=500)
            if answer:
                return {"answer": answer, "sources": hits,
                        "provider": llm.provider_label(), "mode": "ia"}

        # Fallback offline: entrega os trechos recuperados (RAG sem geração).
        return {
            "answer": "Modo offline (sem IA configurada): seguem os trechos mais "
                      "relevantes da base para a sua pergunta.",
            "sources": hits, "provider": llm.provider_label(), "mode": "offline",
        }
