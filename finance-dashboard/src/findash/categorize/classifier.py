"""A small text classifier for transaction descriptions (TF-IDF + Naive Bayes)."""

from __future__ import annotations

from findash.core.categories import UNCATEGORIZED
from findash.utils.formatting import normalize_text


class TransactionClassifier:
    """Wraps a scikit-learn pipeline to predict a category from a description."""

    def __init__(self) -> None:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.naive_bayes import MultinomialNB
        from sklearn.pipeline import Pipeline

        self._pipeline = Pipeline(
            [
                (
                    "tfidf",
                    TfidfVectorizer(
                        preprocessor=normalize_text,
                        ngram_range=(1, 2),
                        min_df=1,
                    ),
                ),
                ("clf", MultinomialNB()),
            ]
        )
        self._fitted = False

    def fit(self, descriptions: list[str], labels: list[str]) -> "TransactionClassifier":
        """Train on labeled descriptions."""
        if descriptions and labels:
            self._pipeline.fit(descriptions, labels)
            self._fitted = True
        return self

    def predict(self, descriptions: list[str]) -> list[str]:
        """Predict categories; falls back to 'uncategorized' when untrained."""
        if not descriptions:
            return []
        if not self._fitted:
            return [UNCATEGORIZED] * len(descriptions)
        return [str(label) for label in self._pipeline.predict(descriptions)]
