"""Flexible CSV statement parser.

Auto-detects the date, description and amount columns by header name and copes
with both Brazilian (``1.234,56``) and US (``1,234.56``) number formats, signed
amount columns or separate debit/credit columns.
"""

from __future__ import annotations

import io

import pandas as pd

from findash.utils.formatting import normalize_text

_DATE_HINTS = ("date", "data")
_DESC_HINTS = (
    "desc", "histor", "memo", "lancamento", "estabelecimento", "nome",
    "detalhe", "transacao", "transaction",
)
_AMOUNT_HINTS = ("valor", "amount", "value", "montante")
_CREDIT_HINTS = ("credito", "entrada", "credit", "deposito")
_DEBIT_HINTS = ("debito", "saida", "debit", "retirada")


def parse_csv(source: bytes | str) -> pd.DataFrame:
    """Parse CSV bytes/str into the canonical transactions DataFrame."""
    text = source.decode("utf-8-sig", errors="replace") if isinstance(source, bytes) else source
    raw = pd.read_csv(
        io.StringIO(text), sep=None, engine="python", dtype=str, skip_blank_lines=True
    )
    raw = raw.dropna(axis=1, how="all")
    columns = {col: normalize_text(str(col)) for col in raw.columns}

    date_col = _find(columns, _DATE_HINTS)
    desc_col = _find(columns, _DESC_HINTS)
    if date_col is None or desc_col is None:
        raise ValueError(
            "Não foi possível identificar as colunas de data e descrição no CSV."
        )

    amount = _extract_amount(raw, columns)
    dates = _parse_dates(raw[date_col])
    descriptions = raw[desc_col].fillna("").astype(str).str.strip()

    df = pd.DataFrame(
        {"date": dates, "description": descriptions, "amount": amount}
    )
    df = df.dropna(subset=["date", "amount"])
    df = df[df["amount"] != 0.0]
    return df.sort_values("date").reset_index(drop=True)


# -- Column detection -------------------------------------------------------
def _find(columns: dict[str, str], hints: tuple[str, ...]) -> str | None:
    for original, normalized in columns.items():
        if any(hint in normalized for hint in hints):
            return original
    return None


def _extract_amount(raw: pd.DataFrame, columns: dict[str, str]) -> pd.Series:
    credit_col = _find(columns, _CREDIT_HINTS)
    debit_col = _find(columns, _DEBIT_HINTS)
    if credit_col is not None and debit_col is not None:
        credit = raw[credit_col].map(parse_amount).fillna(0.0)
        debit = raw[debit_col].map(parse_amount).fillna(0.0)
        return credit - debit.abs()

    amount_col = _find(columns, _AMOUNT_HINTS)
    if amount_col is None:
        raise ValueError("Não foi possível identificar a coluna de valor no CSV.")
    return raw[amount_col].map(parse_amount)


# -- Value parsing ----------------------------------------------------------
def parse_amount(value: object) -> float | None:
    """Parse a monetary string into a float, handling BR/US separators."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text:
        return None

    negative = text.startswith("(") and text.endswith(")")
    cleaned = text.strip("()").replace("R$", "").replace("$", "")
    cleaned = cleaned.replace("\xa0", "").replace(" ", "")
    if cleaned in {"", "-", "+"}:
        return None

    last_dot = cleaned.rfind(".")
    last_comma = cleaned.rfind(",")
    if last_dot != -1 and last_comma != -1:
        # The right-most separator is the decimal one; the other groups thousands.
        decimal_sep, thousand_sep = (".", ",") if last_dot > last_comma else (",", ".")
        cleaned = cleaned.replace(thousand_sep, "").replace(decimal_sep, ".")
    elif last_comma != -1:
        cleaned = cleaned.replace(",", ".")  # comma is the decimal separator

    try:
        number = float(cleaned)
    except ValueError:
        return None
    return -number if negative else number


def _parse_dates(series: pd.Series) -> pd.Series:
    """Parse a date column, preferring day-first (Brazilian) order."""
    dayfirst = pd.to_datetime(series, errors="coerce", dayfirst=True)
    monthfirst = pd.to_datetime(series, errors="coerce", dayfirst=False)
    # Whichever interpretation resolves more values wins.
    return dayfirst if dayfirst.notna().sum() >= monthfirst.notna().sum() else monthfirst
