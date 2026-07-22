"""Statistical outlier detection (z-score or IQR)."""
from __future__ import annotations

import pandas as pd

from .base import BaseDetector


class StatisticalOutlierDetector(BaseDetector):
    name = "statistical_outlier"

    def __init__(self, column: str, method: str = "zscore", threshold: float = 3.0):
        super().__init__(column)
        if method not in ("zscore", "iqr"):
            raise ValueError("method must be 'zscore' or 'iqr'")
        self.method = method
        self.threshold = threshold

    def _detect(self, series: pd.Series) -> pd.Series:
        numeric = pd.to_numeric(series, errors="coerce")
        anomalies = pd.Series(False, index=series.index)
        valid = numeric.dropna()
        if len(valid) < 2:
            return anomalies
        if self.method == "zscore":
            std = valid.std()
            if std == 0:
                return anomalies
            z = (numeric - valid.mean()).abs() / std
            anomalies = z > self.threshold
        else:  # iqr
            q1, q3 = valid.quantile(0.25), valid.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            anomalies = (numeric < lower) | (numeric > upper)
        return anomalies.fillna(False)
