"""Tests for the CSV parser and amount parsing."""

from __future__ import annotations

import pytest

from findash.ingest.csv_parser import parse_amount, parse_csv


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("1.234,56", 1234.56),
        ("1,234.56", 1234.56),
        ("1234.56", 1234.56),
        ("1234,56", 1234.56),
        ("R$ 1.000,00", 1000.0),
        ("-50,00", -50.0),
        ("(50,00)", -50.0),
        ("", None),
        ("-", None),
    ],
)
def test_parse_amount(text: str, expected: float | None) -> None:
    assert parse_amount(text) == expected


def test_parse_csv_brazilian() -> None:
    csv = (
        "Data;Histórico;Valor\n"
        "05/01/2024;Supermercado Pao de Acucar;-150,00\n"
        "06/01/2024;Salario Empresa;5.000,00\n"
        "07/01/2024;Uber Trip;-23,50\n"
    )
    df = parse_csv(csv)
    assert list(df.columns) == ["date", "description", "amount"]
    assert len(df) == 3
    assert df["amount"].tolist() == [-150.0, 5000.0, -23.5]
    assert str(df["date"].dtype).startswith("datetime64")


def test_parse_csv_us_with_debit_credit() -> None:
    csv = (
        "date,description,debit,credit\n"
        "2024-01-05,Grocery,150.00,\n"
        "2024-01-06,Paycheck,,5000.00\n"
    )
    df = parse_csv(csv)
    assert len(df) == 2
    assert df.loc[df["description"] == "Grocery", "amount"].iloc[0] == -150.0
    assert df.loc[df["description"] == "Paycheck", "amount"].iloc[0] == 5000.0
