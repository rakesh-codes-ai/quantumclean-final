"""Generic regex validator."""
from __future__ import annotations

import re
from typing import Union, Pattern

import pandas as pd

from .base import BaseValidator


class RegexValidator(BaseValidator):
    name = "regex"

    def __init__(self, column: str, pattern: Union[str, Pattern], allow_null: bool = True):
        super().__init__(column)
        self.pattern = re.compile(pattern) if isinstance(pattern, str) else pattern
        self.allow_null = allow_null

    def _validate_series(self, series: pd.Series) -> pd.Series:
        nulls = series.isna()
        valid = series.astype(str).str.match(self.pattern)
        valid = valid.where(~nulls, self.allow_null)
        return valid.astype(bool)
