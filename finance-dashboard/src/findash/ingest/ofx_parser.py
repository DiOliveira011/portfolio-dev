"""Minimal OFX/QFX parser (no external dependency).

Works for both SGML (OFX 1.x) and XML (OFX 2.x) because the tags are identical
and values are captured up to the next tag or line break — so closing tags are
optional. Reads the standard ``STMTTRN`` transaction blocks.
"""

from __future__ import annotations

import re
from datetime import datetime

import pandas as pd

_TXN_BLOCK = re.compile(r"<STMTTRN>(.*?)</STMTTRN>", re.IGNORECASE | re.DOTALL)


def _field(block: str, tag: str) -> str | None:
    match = re.search(rf"<{tag}>([^<\r\n]+)", block, re.IGNORECASE)
    return match.group(1).strip() if match else None


def parse_ofx(text: str) -> pd.DataFrame:
    """Parse OFX text into the canonical transactions DataFrame."""
    rows: list[dict[str, object]] = []
    for block in _TXN_BLOCK.findall(text):
        raw_amount = _field(block, "TRNAMT")
        raw_date = _field(block, "DTPOSTED")
        if raw_amount is None or raw_date is None:
            continue
        amount = _to_float(raw_amount)
        when = _to_date(raw_date)
        if amount is None or when is None:
            continue
        description = _field(block, "MEMO") or _field(block, "NAME") or ""
        rows.append({"date": when, "description": description.strip(), "amount": amount})

    if not rows:
        raise ValueError("Nenhuma transação (STMTTRN) encontrada no arquivo OFX.")
    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def _to_float(value: str) -> float | None:
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None


def _to_date(value: str) -> datetime | None:
    digits = value.strip()[:8]
    try:
        return datetime.strptime(digits, "%Y%m%d")
    except ValueError:
        return None
