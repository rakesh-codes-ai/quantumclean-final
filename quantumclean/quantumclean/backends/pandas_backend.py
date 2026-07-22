"""Pandas execution backend."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .base import BaseBackend


class PandasBackend(BaseBackend):
    name = "pandas"

    def _check(self, data: Any) -> pd.DataFrame:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("PandasBackend expects a pandas DataFrame")
        return data

    def num_rows(self, data: Any) -> int:
        return len(self._check(data))

    def get_column(self, data: Any, column: str) -> pd.Series:
        df = self._check(data)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found")
        return df[column]

    def count_nulls(self, data: Any, column: str) -> int:
        return int(self.get_column(data, column).isna().sum())

    def count_unique(self, data: Any, column: str) -> int:
        return int(self.get_column(data, column).nunique())
