"""Data lineage: a diary of where data came from and what happened to it."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class LineageEvent:
    operation: str
    timestamp: str
    details: Dict[str, Any] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"<LineageEvent {self.operation} @ {self.timestamp}>"


class LineageTracker:
    """Records sources and operations applied to a dataset, in order."""

    def __init__(self, dataset_name: str):
        if not isinstance(dataset_name, str) or not dataset_name:
            raise ValueError("dataset_name must be a non-empty string")
        self.dataset_name = dataset_name
        self._sources: List[str] = []
        self._events: List[LineageEvent] = []

    @staticmethod
    def _now() -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    def add_source(self, source: str) -> "LineageTracker":
        if not source:
            raise ValueError("source must be a non-empty string")
        self._sources.append(source)
        self._events.append(
            LineageEvent("source_added", self._now(), {"source": source})
        )
        return self

    def record(self, operation: str, **details: Any) -> "LineageTracker":
        if not operation:
            raise ValueError("operation must be a non-empty string")
        self._events.append(LineageEvent(operation, self._now(), dict(details)))
        return self

    @property
    def sources(self) -> List[str]:
        return list(self._sources)

    @property
    def events(self) -> List[LineageEvent]:
        return list(self._events)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset": self.dataset_name,
            "sources": self.sources,
            "events": [
                {"operation": e.operation, "timestamp": e.timestamp, "details": e.details}
                for e in self._events
            ],
        }

    def summary(self) -> str:
        lines = [f"Lineage for '{self.dataset_name}'", "-" * 40]
        lines += [f"Source: {s}" for s in self._sources] or ["Source: (none recorded)"]
        for e in self._events:
            if e.operation != "source_added":
                extra = f" {e.details}" if e.details else ""
                lines.append(f"{e.timestamp}  {e.operation}{extra}")
        return "\n".join(lines)

    def __repr__(self) -> str:
        return f"<LineageTracker '{self.dataset_name}' events={len(self._events)}>"
