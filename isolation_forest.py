"""Email validator using an RFC-pragmatic regex."""
from __future__ import annotations

import re

import pandas as pd

from .base import BaseValidator

_EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class EmailValidator(BaseValidator):
    name = "email"

    def __init__(self, column: str, allow_null: bool = True):
        super().__init__(column)
        self.allow_null = allow_null

    def _validate_series(self, series: pd.Series) -> pd.Series:
        nulls = series.isna()
        valid = series.astype(str).str.match(_EMAIL_RE)
        valid = valid.where(~nulls, self.allow_null)
        return valid.astype(bool)
