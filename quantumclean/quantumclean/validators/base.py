"""Abstract base class for all validators (plugin contract)."""
from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from ..results import ValidationResult


class BaseValidator(ABC):
    """Contract every validator must implement.

    Subclasses implement ``_validate_series`` which returns a boolean
    Series (True = the value is VALID). The public ``validate`` method
    handles column lookup and result construction so all validators
    behave consistently. This is the extension point that lets users
    add custom validators without touching core code.
    """

    name: str = "base"

    def __init__(self, column: str):
        if not isinstance(column, str) or not column:
            raise ValueError("column must be a non-empty string")
        self.column = column

    @abstractmethod
    def _validate_series(self, series: pd.Series) -> pd.Series:
        """Return a boolean Series aligned to ``series``; True = valid."""
        raise NotImplementedError

    def validate(self, df: pd.DataFrame) -> ValidationResult:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
        if self.column not in df.columns:
            raise KeyError(f"Column '{self.column}' not found in DataFrame")
        series = df[self.column]
        mask = self._validate_series(series).astype(bool)
        failed_indices = series.index[~mask].tolist()
        return ValidationResult(
            column=self.column,
            validator=self.name,
            total=len(series),
            failed_indices=failed_indices,
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} column='{self.column}'>"
