"""Result objects returned by validators and schemas."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class ValidationResult:
    """Outcome of running a single validator against one column."""

    column: str
    validator: str
    total: int
    failed_indices: List[Any] = field(default_factory=list)

    @property
    def failed(self) -> int:
        return len(self.failed_indices)

    @property
    def passed(self) -> int:
        return self.total - self.failed

    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 1.0
        return self.passed / self.total

    @property
    def is_valid(self) -> bool:
        return self.failed == 0

    def __repr__(self) -> str:
        status = "PASS" if self.is_valid else "FAIL"
        return (
            f"<ValidationResult {self.validator} on '{self.column}': {status} "
            f"({self.passed}/{self.total} passed, {self.pass_rate:.1%})>"
        )


@dataclass
class SchemaResult:
    """Aggregated outcome of running a Schema (many validators)."""

    results: List[ValidationResult] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return all(r.is_valid for r in self.results)

    @property
    def pass_rate(self) -> float:
        if not self.results:
            return 1.0
        return sum(r.pass_rate for r in self.results) / len(self.results)

    def failures(self) -> List[ValidationResult]:
        return [r for r in self.results if not r.is_valid]

    def summary(self) -> str:
        header = "PASSED" if self.is_valid else "FAILED"
        lines = [
            f"Schema validation: {header}",
            f"Overall pass rate: {self.pass_rate:.1%}",
            f"Validators run:    {len(self.results)}",
            "-" * 52,
        ]
        for r in self.results:
            status = "PASS" if r.is_valid else "FAIL"
            lines.append(
                f"[{status}] {r.validator:<12} {r.column:<15} "
                f"{r.passed}/{r.total} ({r.pass_rate:.1%})"
            )
        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "pass_rate": self.pass_rate,
            "results": [
                {
                    "column": r.column,
                    "validator": r.validator,
                    "total": r.total,
                    "passed": r.passed,
                    "failed": r.failed,
                    "pass_rate": r.pass_rate,
                    "failed_indices": r.failed_indices,
                    "is_valid": r.is_valid,
                }
                for r in self.results
            ],
        }

    def __repr__(self) -> str:
        status = "PASS" if self.is_valid else "FAIL"
        return f"<SchemaResult {status} pass_rate={self.pass_rate:.1%} validators={len(self.results)}>"
