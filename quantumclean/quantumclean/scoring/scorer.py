"""Multi-metric data quality scoring."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

import pandas as pd


@dataclass
class QualityScore:
    completeness: float
    uniqueness: float
    validity: float
    consistency: float
    weights: Dict[str, float] = field(default_factory=dict)

    @property
    def overall(self) -> float:
        metrics = {
            "completeness": self.completeness,
            "uniqueness": self.uniqueness,
            "validity": self.validity,
            "consistency": self.consistency,
        }
        total_w = sum(self.weights.values())
        if total_w == 0:
            return sum(metrics.values()) / len(metrics)
        return sum(metrics[k] * w for k, w in self.weights.items()) / total_w

    def to_dict(self) -> Dict[str, float]:
        return {
            "completeness": round(self.completeness, 4),
            "uniqueness": round(self.uniqueness, 4),
            "validity": round(self.validity, 4),
            "consistency": round(self.consistency, 4),
            "overall": round(self.overall, 4),
        }

    def summary(self) -> str:
        d = self.to_dict()
        lines = ["Data Quality Score", "-" * 32]
        for k in ("completeness", "uniqueness", "validity", "consistency"):
            lines.append(f"{k.capitalize():<14} {d[k]:.1%}")
        lines.append("-" * 32)
        lines.append(f"{'OVERALL':<14} {d['overall']:.1%}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<QualityScore overall={self.overall:.1%}>"


class QualityScorer:
    """Compute completeness, uniqueness, validity and consistency for a DataFrame."""

    DEFAULT_WEIGHTS = {
        "completeness": 1.0,
        "uniqueness": 1.0,
        "validity": 1.0,
        "consistency": 1.0,
    }

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = dict(weights) if weights else dict(self.DEFAULT_WEIGHTS)

    @staticmethod
    def _completeness(df: pd.DataFrame) -> float:
        if df.size == 0:
            return 1.0
        return float(df.notna().sum().sum() / df.size)

    @staticmethod
    def _uniqueness(df: pd.DataFrame) -> float:
        rates = []
        for col in df.columns:
            non_null = df[col].notna().sum()
            if non_null == 0:
                rates.append(1.0)
            else:
                rates.append(min(df[col].nunique() / non_null, 1.0))
        return float(sum(rates) / len(rates)) if rates else 1.0

    @staticmethod
    def _consistency(df: pd.DataFrame) -> float:
        rates = []
        for col in df.columns:
            non_null = df[col].dropna()
            if len(non_null) == 0:
                rates.append(1.0)
                continue
            types = non_null.map(lambda v: type(v).__name__)
            dominant = types.value_counts().iloc[0]
            rates.append(dominant / len(non_null))
        return float(sum(rates) / len(rates)) if rates else 1.0

    def score(self, df: pd.DataFrame, schema=None) -> QualityScore:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
        validity = 1.0
        if schema is not None:
            validity = schema.validate(df).pass_rate
        return QualityScore(
            completeness=self._completeness(df),
            uniqueness=self._uniqueness(df),
            validity=validity,
            consistency=self._consistency(df),
            weights=dict(self.weights),
        )
