"""LLM provider layer: Groq (grátis) ou Claude (Anthropic), via stdlib urllib.

Sem SDKs: as chamadas usam urllib. É *offline-safe*: se não houver chave (ou a
rede falhar), `complete()` devolve None e o app usa o modo offline.

Variáveis de ambiente:
    GROQ_API_KEY        habilita o Groq (gratuito).
    ANTHROPIC_API_KEY   habilita o Claude.
    LLM_PROVIDER        força "groq" ou "claude" quando ambas as chaves existem.
    GROQ_MODEL / ANTHROPIC_MODEL  sobrescrevem o modelo padrão.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-6"
DEFAULT_GROQ_MODEL = "llama-3.3-70b-versatile"


def provider() -> str | None:
    """Return the active provider: 'claude', 'groq' or None (offline)."""
    forced = (os.getenv("LLM_PROVIDER") or "").strip().lower()
    if forced == "claude" and os.getenv("ANTHROPIC_API_KEY"):
        return "claude"
    if forced == "groq" and os.getenv("GROQ_API_KEY"):
        return "groq"
    if os.getenv("ANTHROPIC_API_KEY"):
        return "claude"
    if os.getenv("GROQ_API_KEY"):
        return "groq"
    return None


def provider_label() -> str:
    return {"claude": "Claude (Anthropic)", "groq": "Groq (Llama)"}.get(
        provider(), "Offline (sem IA)"
    )


def available() -> bool:
    return provider() is not None


def _post(url: str, headers: dict, payload: dict, timeout: int = 45) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (URL fixa/HTTPS)
        return json.loads(resp.read().decode("utf-8"))


def _claude(system: str, user: str, max_tokens: int, temperature: float) -> str:
    headers = {
        "x-api-key": os.environ["ANTHROPIC_API_KEY"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": os.getenv("ANTHROPIC_MODEL", DEFAULT_ANTHROPIC_MODEL),
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    out = _post(ANTHROPIC_URL, headers, payload)
    return "".join(
        b.get("text", "") for b in out.get("content", []) if b.get("type") == "text"
    ).strip()


def _groq(system: str, user: str, max_tokens: int, temperature: float) -> str:
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "content-type": "application/json",
    }
    payload = {
        "model": os.getenv("GROQ_MODEL", DEFAULT_GROQ_MODEL),
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    out = _post(GROQ_URL, headers, payload)
    return out["choices"][0]["message"]["content"].strip()


def complete(system: str, user: str, *, max_tokens: int = 600,
             temperature: float = 0.3) -> str | None:
    """Return the model's text, or None if offline / on any failure."""
    active = provider()
    try:
        if active == "claude":
            return _claude(system, user, max_tokens, temperature) or None
        if active == "groq":
            return _groq(system, user, max_tokens, temperature) or None
    except (urllib.error.URLError, KeyError, ValueError, TimeoutError, OSError):
        return None
    return None
