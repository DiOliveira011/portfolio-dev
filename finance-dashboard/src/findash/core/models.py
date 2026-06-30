"""Domain model for a financial transaction."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


class TransactionType(str, Enum):
    """Direction of money flow."""

    INCOME = "income"
    EXPENSE = "expense"


@dataclass(slots=True)
class Transaction:
    """A single normalized transaction.

    ``amount`` is **signed**: positive = money in (income/credit),
    negative = money out (expense/debit).
    """

    date: date
    description: str
    amount: float
    category: str | None = None
    account: str | None = None
    source: str | None = None

    @property
    def type(self) -> TransactionType:
        return TransactionType.INCOME if self.amount >= 0 else TransactionType.EXPENSE

    @property
    def is_expense(self) -> bool:
        return self.amount < 0

    @property
    def abs_amount(self) -> float:
        """Magnitude of the transaction, always non-negative."""
        return abs(self.amount)
