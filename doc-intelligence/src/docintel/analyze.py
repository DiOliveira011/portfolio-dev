"""Text analytics: stats, keywords and extractive summary (pure Python)."""

from __future__ import annotations

import re
import unicodedata
from collections import Counter

_STOP = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "nao", "uma",
    "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "ao", "ele",
    "das", "seu", "sua", "ou", "quando", "muito", "nos", "ja", "eu", "tambem", "so",
    "pelo", "pela", "ate", "isso", "ela", "entre", "sem", "mesmo", "aos", "seus",
    "quem", "nas", "me", "esse", "eles", "voce", "essa", "num", "nem", "meu", "minha",
    "tem", "ser", "foi", "sao", "esta", "este", "estao", "pelos", "pelas", "the",
}

_WORD = re.compile(r"[0-9A-Za-zÀ-ÿ]+")
_SENT = re.compile(r"[^.!?\n]+[.!?]?")


def _norm(word: str) -> str:
    word = unicodedata.normalize("NFKD", word.lower())
    return "".join(c for c in word if not unicodedata.combining(c))


def words(text: str) -> list[str]:
    return _WORD.findall(text)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENT.findall(text) if len(s.strip()) > 2]


def tokens(text: str) -> list[str]:
    return [n for w in words(text) if len(n := _norm(w)) >= 3 and n not in _STOP]


def stats(text: str) -> dict:
    ws = words(text)
    return {
        "caracteres": len(text),
        "palavras": len(ws),
        "frases": len(sentences(text)),
        "palavras_unicas": len({_norm(w) for w in ws}),
        "tempo_leitura_min": max(1, round(len(ws) / 200)) if ws else 0,
    }


def keywords(text: str, n: int = 10) -> list[tuple[str, int]]:
    return Counter(tokens(text)).most_common(n)


def extractive_summary(text: str, n: int = 3) -> str:
    sents = sentences(text)
    if len(sents) <= n:
        return " ".join(sents)
    freq = Counter(tokens(text))
    scored = []
    for i, s in enumerate(sents):
        toks = tokens(s)
        score = sum(freq[t] for t in toks) / (len(toks) + 1)
        scored.append((score, i, s))
    best = sorted(scored, reverse=True)[:n]
    return " ".join(s for _, _, s in sorted(best, key=lambda x: x[1]))
