"""Transaction categorization: keyword rules + an ML text classifier.

Rules label whatever they confidently can; the classifier then trains on those
rule-labeled rows and predicts categories for the ones the rules missed. This
"self-training" approach needs no external labeled dataset.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from findash.categorize.classifier import TransactionClassifier
from findash.categorize.rules import categorize_by_rules
from findash.core.categories import UNCATEGORIZED

__all__ = [
    "TransactionClassifier",
    "categorize_by_rules",
    "categorize_dataframe",
    "CategorizationResult",
]

_MIN_LABELED_FOR_ML = 12


@dataclass(slots=True)
class CategorizationResult:
    """Outcome of categorizing a transactions DataFrame."""

    df: pd.DataFrame
    by_rules: int
    by_ml: int
    uncategorized: int


def categorize_dataframe(df: pd.DataFrame, *, use_ml: bool = True) -> CategorizationResult:
    """Return ``df`` with a ``category`` column plus categorization stats."""
    result = df.copy()
    result["category"] = [
        categorize_by_rules(desc, amount)
        for desc, amount in zip(result["description"], result["amount"], strict=False)
    ]

    by_rules = int(result["category"].notna().sum())
    by_ml = 0

    missing = result["category"].isna()
    labeled = result.loc[~missing]
    if (
        use_ml
        and missing.any()
        and labeled["category"].nunique() >= 2
        and len(labeled) >= _MIN_LABELED_FOR_ML
    ):
        classifier = TransactionClassifier()
        classifier.fit(labeled["description"].tolist(), labeled["category"].tolist())
        predictions = classifier.predict(result.loc[missing, "description"].tolist())
        result.loc[missing, "category"] = predictions
        by_ml = int(missing.sum())

    uncategorized_mask = result["category"].isna()
    uncategorized = int(uncategorized_mask.sum())
    result.loc[uncategorized_mask, "category"] = UNCATEGORIZED

    return CategorizationResult(
        df=result, by_rules=by_rules, by_ml=by_ml, uncategorized=uncategorized
    )
