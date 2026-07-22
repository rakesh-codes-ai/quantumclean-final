"""Uniqueness validator: flags every member of a duplicated group."""
from __future__ import annotations

import pandas as pd

from .base import BaseValidator


class UniqueValidator(BaseValidator):
    name = "unique"

    def __init__(self, column: str, ignore_null: bool = True):
        super().__init__(column)
        self.ignore_null = ignore_null

    def _validate_series(self, series: pd.Series) -> pd.Series:
        valid = ~series.duplicated(keep=False)
        if self.ignore_null:
            valid = valid | series.isna()
        return valid
