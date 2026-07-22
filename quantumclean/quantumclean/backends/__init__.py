"""Execution backends for QuantumClean (strategy + factory patterns)."""
from .base import BaseBackend
from .duckdb_backend import DuckDBBackend
from .pandas_backend import PandasBackend
from .spark_backend import SparkBackend

_BACKENDS = {
    "pandas": PandasBackend,
    "duckdb": DuckDBBackend,
    "spark": SparkBackend,
}


def get_backend(name: str = "pandas") -> BaseBackend:
    """Factory: return a backend instance by name."""
    key = name.lower()
    if key not in _BACKENDS:
        raise ValueError(f"Unknown backend '{name}'. Available: {sorted(_BACKENDS)}")
    return _BACKENDS[key]()


__all__ = ["BaseBackend", "PandasBackend", "DuckDBBackend", "SparkBackend", "get_backend"]
