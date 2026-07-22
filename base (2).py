"""NotNull validator: flags missing values."""
from __future__ import annotations

import pandas as pd

from .base import BaseValidator


class NotNullValidator(BaseValidator):
    name = "not_null"

    def _validate_series(self, series: pd.Series) -> pd.Series:
        return series.notna()
