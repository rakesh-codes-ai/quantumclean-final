"""Apache Spark execution backend for distributed datasets.

The import is lazy so the rest of the library works without Spark
installed. Install with: pip install pyspark (requires Java 8+).
"""
from __future__ import annotations

from typing import Any

from .base import BaseBackend


class SparkBackend(BaseBackend):
    name = "spark"

    @staticmethod
    def _require_spark():
        try:
            from pyspark.sql import DataFrame as SparkDataFrame  # noqa: F401
            from pyspark.sql import functions as F  # noqa: F401
        except ImportError as exc:
            raise ImportError(
                "SparkBackend requires pyspark. Install it with: "
                "pip install 'quantumclean[spark]' (needs Java 8+)."
            ) from exc

    def _check(self, data: Any):
        self._require_spark()
        from pyspark.sql import DataFrame as SparkDataFrame

        if not isinstance(data, SparkDataFrame):
            raise TypeError("SparkBackend expects a Spark DataFrame")
        return data

    def num_rows(self, data: Any) -> int:
        return int(self._check(data).count())

    def get_column(self, data: Any, column: str):
        df = self._check(data)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found")
        return df.select(column)

    def count_nulls(self, data: Any, column: str) -> int:
        df = self._check(data)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found")
        from pyspark.sql import functions as F

        return int(df.filter(F.col(column).isNull()).count())

    def count_unique(self, data: Any, column: str) -> int:
        df = self._check(data)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found")
        return int(df.select(column).distinct().count())
