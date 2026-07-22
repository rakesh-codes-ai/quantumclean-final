"""Quality SLA: an automated contract that data quality must meet."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from ..scoring.scorer import QualityScore


@dataclass
class SLABreach:
    metric: str
    threshold: float
    actual: float

    def __repr__(self) -> str:
        return f"<SLABreach {self.metric}: required {self.threshold:.1%}, got {self.actual:.1%}>"


@dataclass
class SLAReport:
    breaches: List[SLABreach] = field(default_factory=list)
    checked: Dict[str, float] = field(default_factory=dict)

    @property
    def is_met(self) -> bool:
        return len(self.breaches) == 0

    def summary(self) -> str:
        status = "SLA MET ✔" if self.is_met else "SLA BREACHED ✘"
        lines = [f"Quality SLA check: {status}", "-" * 40]
        for metric, threshold in self.checked.items():
            breach = next((b for b in self.breaches if b.metric == metric), None)
            if breach:
                lines.append(f"[FAIL] {metric:<13} needs {threshold:.1%}, got {breach.actual:.1%}")
            else:
                lines.append(f"[ OK ] {metric:<13} needs {threshold:.1%}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<SLAReport met={self.is_met} breaches={len(self.breaches)}>"


class QualitySLA:
    """Define minimum quality thresholds and check scores against them."""

    def __init__(
        self,
        min_overall: Optional[float] = None,
        min_completeness: Optional[float] = None,
        min_uniqueness: Optional[float] = None,
        min_validity: Optional[float] = None,
        min_consistency: Optional[float] = None,
    ):
        self.thresholds: Dict[str, float] = {}
        for name, value in (
            ("overall", min_overall),
            ("completeness", min_completeness),
            ("uniqueness", min_uniqueness),
            ("validity", min_validity),
            ("consistency", min_consistency),
        ):
            if value is not None:
                if not 0 <= value <= 1:
                    raise ValueError(f"{name} threshold must be between 0 and 1")
                self.thresholds[name] = value
        if not self.thresholds:
            raise ValueError("At least one threshold must be provided")

    def check(self, score: QualityScore) -> SLAReport:
        if not isinstance(score, QualityScore):
            raise TypeError("check() expects a QualityScore")
        actuals = {
            "overall": score.overall,
            "completeness": score.completeness,
            "uniqueness": score.uniqueness,
            "validity": score.validity,
            "consistency": score.consistency,
        }
        breaches = [
            SLABreach(metric=m, threshold=t, actual=actuals[m])
            for m, t in self.thresholds.items()
            if actuals[m] < t
        ]
        return SLAReport(breaches=breaches, checked=dict(self.thresholds))

    def __repr__(self) -> str:
        return f"<QualitySLA thresholds={self.thresholds}>"
