"""Tiny TF-IDF retriever (pure Python, no numpy/sklearn)."""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

_STOP = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "com", "nao", "uma",
    "os", "no", "se", "na", "por", "mais", "as", "dos", "como", "mas", "ao", "ele",
    "das", "seu", "sua", "ou", "quando", "muito", "nos", "ja", "eu", "tambem", "so",
    "pelo", "pela", "ate", "isso", "ela", "entre", "sem", "mesmo", "aos", "seus",
    "quem", "nas", "me", "esse", "eles", "voce", "essa", "num", "nem", "meu", "minha",
    "tem", "ter", "qual", "quais", "onde", "quanto", "quantos", "quantas", "posso",
    "sobre", "ser", "the", "is",
}


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", normalize(text))
            if len(t) >= 2 and t not in _STOP]


class Retriever:
    """Index documents and retrieve the most relevant by cosine similarity."""

    def __init__(self, docs: dict[str, str]) -> None:
        self.titles = list(docs)
        self.texts = list(docs.values())
        chunks = [f"{t}. {b}" for t, b in docs.items()]
        self._tokens = [tokenize(c) for c in chunks]

        df: Counter[str] = Counter()
        for toks in self._tokens:
            df.update(set(toks))
        n = len(chunks)
        self.idf = {term: math.log((n + 1) / (dft + 1)) + 1.0 for term, dft in df.items()}
        self._vectors = [self._vector(toks) for toks in self._tokens]

    def _vector(self, tokens: list[str]) -> dict[str, float]:
        tf = Counter(tokens)
        vec = {term: count * self.idf.get(term, 0.0) for term, count in tf.items()}
        norm = math.sqrt(sum(w * w for w in vec.values())) or 1.0
        return {term: w / norm for term, w in vec.items()}

    def retrieve(self, query: str, k: int = 3) -> list[dict]:
        q = self._vector(tokenize(query))
        if not q:
            return []
        scored = []
        for i, vec in enumerate(self._vectors):
            score = sum(q.get(term, 0.0) * w for term, w in vec.items())
            if score > 0:
                scored.append((score, i))
        scored.sort(reverse=True)
        return [
            {"title": self.titles[i], "text": self.texts[i], "score": round(score, 3)}
            for score, i in scored[:k]
        ]
