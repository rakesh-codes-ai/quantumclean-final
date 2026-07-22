"""Isolation Forest anomaly detection (scikit-learn based)."""
from __future__ import annotations

import pandas as pd

from .base import BaseDetector


class IsolationForestDetector(BaseDetector):
    name = "isolation_forest"

    def __init__(self, column: str, contamination: float = 0.1, random_state: int = 42):
        super().__init__(column)
        self.contamination = contamination
        self.random_state = random_state

    def _detect(self, series: pd.Series) -> pd.Series:
        try:
            from sklearn.ensemble import IsolationForest
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "IsolationForestDetector requires scikit-learn. "
                "Install it with: pip install 'quantumclean[ml]'"
            ) from exc

        numeric = pd.to_numeric(series, errors="coerce")
        anomalies = pd.Series(False, index=series.index)
        mask_valid = numeric.notna()
        valid = numeric[mask_valid]
        if len(valid) < 2:
            return anomalies
        model = IsolationForest(
            contamination=self.contamination, random_state=self.random_state
        )
        preds = model.fit_predict(valid.values.reshape(-1, 1))
        anomalies.loc[valid.index] = preds == -1
        return anomalies
