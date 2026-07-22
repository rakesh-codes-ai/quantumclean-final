"""QuantumClean: a production-grade, extensible data quality library."""
from .results import SchemaResult, ValidationResult
from .schema import Schema
from .validators import (
    BaseValidator,
    CategoricalValidator,
    EmailValidator,
    NotNullValidator,
    RangeValidator,
    RegexValidator,
    UniqueValidator,
)
from .detectors import (
    BaseDetector,
    DetectionResult,
    StatisticalOutlierDetector,
    IsolationForestDetector,
)
from .scoring import QualityScore, QualityScorer
from .backends import (
    BaseBackend,
    PandasBackend,
    DuckDBBackend,
    SparkBackend,
    get_backend,
)
from .lineage import LineageEvent, LineageTracker
from .sla import QualitySLA, SLABreach, SLAReport

__version__ = "1.0.0"

__all__ = [
    # core (Sprint 1)
    "Schema", "SchemaResult", "ValidationResult",
    "BaseValidator", "CategoricalValidator", "EmailValidator",
    "NotNullValidator", "RangeValidator", "RegexValidator", "UniqueValidator",
    # detectors (Sprint 2)
    "BaseDetector", "DetectionResult",
    "StatisticalOutlierDetector", "IsolationForestDetector",
    # scoring (Sprint 2)
    "QualityScore", "QualityScorer",
    # backends (Sprint 2 + 3)
    "BaseBackend", "PandasBackend", "DuckDBBackend", "SparkBackend", "get_backend",
    # lineage + SLA (Sprint 3)
    "LineageEvent", "LineageTracker",
    "QualitySLA", "SLABreach", "SLAReport",
    "__version__",
]
