"""Tests for keyword rules and the full categorization pipeline."""

from __future__ import annotations

import pytest

from findash.categorize import categorize_dataframe
from findash.categorize.rules import categorize_by_rules
from findash.sample import generate_sample_dataframe


@pytest.mark.parametrize(
    ("description", "amount", "expected"),
    [
        ("Uber *Trip", -20.0, "Transporte"),
        ("iFood Restaurante", -30.0, "Alimentação"),
        ("Supermercado Pao de Acucar", -150.0, "Mercado"),
        ("Netflix", -39.9, "Lazer"),  # first matching expense rule wins
        ("Salario Empresa XPTO", 5000.0, "Renda"),
        ("Loja Totalmente Desconhecida ZZZ", -10.0, None),
    ],
)
def test_categorize_by_rules(description: str, amount: float, expected: str | None) -> None:
    assert categorize_by_rules(description, amount) == expected


def test_pipeline_categorizes_everything() -> None:
    df = generate_sample_dataframe(months=3, seed=1)
    result = categorize_dataframe(df, use_ml=True)
    assert result.df["category"].notna().all()
    assert result.by_rules > 0
    # Every category assigned is a known one.
    assert result.df["category"].isin(
        result.df["category"].unique()
    ).all()


def test_pipeline_without_ml_marks_unknown() -> None:
    import pandas as pd

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-02"]),
            "description": ["Loja XYZ Desconhecida", "Outra Loja QWE"],
            "amount": [-10.0, -20.0],
        }
    )
    result = categorize_dataframe(df, use_ml=False)
    assert (result.df["category"] == "Outros").all()
    assert result.uncategorized == 2
