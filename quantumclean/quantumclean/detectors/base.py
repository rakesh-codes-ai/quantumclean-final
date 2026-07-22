"""Abstract base class for anomaly detectors (plugin contract)."""
from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from .results import DetectionResult


class BaseDetector(ABC):
    """Every detector returns a boolean mask: True = anomaly."""

    name: str = "base"

    def __init__(self, column: str):
        if not isinstance(column, str) or not column:
            raise ValueError("column must be a non-empty string")
        self.column = column

    @abstractmethod
    def _detect(self, series: pd.Series) -> pd.Series:
        """Return a boolean Series aligned to ``series``; True = anomaly."""
        raise NotImplementedError

    def detect(self, df: pd.DataFrame) -> DetectionResult:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
        if self.column not in df.columns:
            raise KeyError(f"Column '{self.column}' not found in DataFrame")
        series = df[self.column]
        mask = self._detect(series).astype(bool)
        anomaly_indices = series.index[mask].tolist()
        return DetectionResult(
            column=self.column,
            detector=self.name,
            total=len(series),
            anomaly_indices=anomaly_indices,
        )

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} column='{self.column}'>"
