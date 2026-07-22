"""Numeric range validator."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from .base import BaseValidator


class RangeValidator(BaseValidator):
    name = "range"

    def __init__(
        self,
        column: str,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        inclusive: bool = True,
        allow_null: bool = True,
    ):
        super().__init__(column)
        if min_value is None and max_value is None:
            raise ValueError("At least one of min_value or max_value must be provided")
        self.min_value = min_value
        self.max_value = max_value
        self.inclusive = inclusive
        self.allow_null = allow_null

    def _validate_series(self, series: pd.Series) -> pd.Series:
        nulls = series.isna()
        numeric = pd.to_numeric(series, errors="coerce")
        valid = pd.Series(True, index=series.index)
        if self.min_value is not None:
            valid &= (numeric >= self.min_value) if self.inclusive else (numeric > self.min_value)
        if self.max_value is not None:
            valid &= (numeric <= self.max_value) if self.inclusive else (numeric < self.max_value)
        # Non-numeric, non-null values cannot be in range.
        valid &= ~(numeric.isna() & ~nulls)
        if self.allow_null:
            valid = valid | nulls
        else:
            valid = valid & ~nulls
        return valid
