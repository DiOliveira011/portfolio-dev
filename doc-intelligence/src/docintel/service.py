"""Tie extraction + analysis + summarization together."""

from __future__ import annotations

from docintel import llm
from docintel.analyze import extractive_summary, keywords, stats

_SYSTEM = (
    "Você é um analista que resume documentos em português do Brasil. "
    "Produza, em markdown simples: um TÍTULO curto (linha começando com '# '), "
    "um RESUMO de 2 a 3 frases e 3 a 5 PONTOS-CHAVE em bullets ('- '). "
    "Seja fiel ao conteúdo; não invente informação."
)


def analyze_text(text: str) -> dict:
    return {
        "stats": stats(text),
        "keywords": keywords(text, 10),
        "extractive": extractive_summary(text, 3),
    }


def summarize(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {"mode": "vazio", "provider": llm.provider_label(), "summary": "", "bullets": []}
    if llm.available():
        out = llm.complete(_SYSTEM, f"Documento:\n\n{text[:6000]}",
                           max_tokens=600, temperature=0.3)
        if out:
            return {"mode": "ia", "provider": llm.provider_label(),
                    "summary": out, "bullets": []}
    return {
        "mode": "offline",
        "provider": llm.provider_label(),
        "summary": extractive_summary(text, 3),
        "bullets": [k for k, _ in keywords(text, 5)],
    }
