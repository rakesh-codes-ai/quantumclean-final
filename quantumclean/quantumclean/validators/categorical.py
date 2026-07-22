"""Categorical (allowed-values) validator."""
from __future__ import annotations

from typing import Iterable

import pandas as pd

from .base import BaseValidator


class CategoricalValidator(BaseValidator):
    name = "categorical"

    def __init__(self, column: str, categories: Iterable, allow_null: bool = True):
        super().__init__(column)
        categories = list(categories)
        if not categories:
            raise ValueError("categories must be a non-empty collection")
        self.categories = set(categories)
        self.allow_null = allow_null

    def _validate_series(self, series: pd.Series) -> pd.Series:
        valid = series.isin(self.categories)
        if self.allow_null:
            valid = valid | series.isna()
        return valid
