"""Result object for anomaly detection."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class DetectionResult:
    column: str
    detector: str
    total: int
    anomaly_indices: List[Any] = field(default_factory=list)

    @property
    def anomaly_count(self) -> int:
        return len(self.anomaly_indices)

    @property
    def normal_count(self) -> int:
        return self.total - self.anomaly_count

    @property
    def anomaly_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.anomaly_count / self.total

    def __repr__(self) -> str:
        return (
            f"<DetectionResult {self.detector} on '{self.column}': "
            f"{self.anomaly_count}/{self.total} anomalies ({self.anomaly_rate:.1%})>"
        )
