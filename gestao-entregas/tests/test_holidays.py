"""Tests for holidays and business-day math."""

from __future__ import annotations

from datetime import date

from gentregas.holidays import add_business_days, easter, is_business_day


def test_easter_dates() -> None:
    assert easter(2024) == date(2024, 3, 31)
    assert easter(2025) == date(2025, 4, 20)
    assert easter(2026) == date(2026, 4, 5)


def test_is_business_day() -> None:
    assert is_business_day(date(2025, 1, 2)) is True          # quinta normal
    assert is_business_day(date(2025, 1, 4)) is False         # sábado
    assert is_business_day(date(2025, 1, 1)) is False         # feriado (Ano Novo)
    assert is_business_day(date(2025, 4, 21)) is False        # Tiradentes


def test_add_business_days_skips_weekend() -> None:
    # sexta + 1 dia útil = segunda
    assert add_business_days(date(2025, 1, 3), 1) == date(2025, 1, 6)


def test_add_business_days_skips_holiday() -> None:
    # quarta 24/12 + 1 dia útil pula o Natal (25/12) -> sexta 26/12
    assert add_business_days(date(2025, 12, 24), 1) == date(2025, 12, 26)
