"""Brazilian holidays and business-day math (for SLA / prazos).

Computes national holidays (fixed + Easter-based) and advances dates by *working
days*, skipping weekends and holidays — the same logic an operations team needs
to know "que horas/dia tem que entregar". Adapted from a production tool.
"""

from __future__ import annotations

from datetime import date, timedelta
from functools import lru_cache

# National fixed holidays: (month, day).
_NATIONAL_FIXED = [
    (1, 1),    # Confraternização Universal
    (4, 21),   # Tiradentes
    (5, 1),    # Dia do Trabalho
    (9, 7),    # Independência
    (10, 12),  # N. Sra. Aparecida
    (11, 2),   # Finados
    (11, 15),  # Proclamação da República
    (11, 20),  # Consciência Negra (nacional a partir de 2024)
    (12, 25),  # Natal
]


def easter(year: int) -> date:
    """Date of Easter Sunday (anonymous Gregorian algorithm)."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    el = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * el) // 451
    month = (h + el - 7 * m + 114) // 31
    day = ((h + el - 7 * m + 114) % 31) + 1
    return date(year, month, day)


@lru_cache(maxsize=64)
def holidays(year: int) -> frozenset[date]:
    """All recognised holidays for ``year`` (fixed + Easter-based)."""
    days: set[date] = set()
    for month, day in _NATIONAL_FIXED:
        if month == 11 and day == 20 and year < 2024:
            continue
        days.add(date(year, month, day))
    e = easter(year)
    days.add(e - timedelta(days=48))  # Carnaval (segunda)
    days.add(e - timedelta(days=47))  # Carnaval (terça)
    days.add(e - timedelta(days=2))   # Sexta-feira da Paixão
    days.add(e + timedelta(days=60))  # Corpus Christi
    return frozenset(days)


def is_business_day(day: date) -> bool:
    """``True`` if ``day`` is a weekday and not a holiday."""
    return day.weekday() < 5 and day not in holidays(day.year)


def add_business_days(start: date, n: int) -> date:
    """Return the date ``n`` business days after ``start``."""
    day = start
    remaining = n
    while remaining > 0:
        day += timedelta(days=1)
        if is_business_day(day):
            remaining -= 1
    return day
