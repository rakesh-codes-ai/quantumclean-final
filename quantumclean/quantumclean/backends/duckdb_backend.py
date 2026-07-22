"""DuckDB execution backend: runs SQL over pandas DataFrames."""
from __future__ import annotations

from typing import Any

import pandas as pd

from .base import BaseBackend


class DuckDBBackend(BaseBackend):
    name = "duckdb"

    def _connect(self):
        try:
            import duckdb
        except ImportError as exc:  # pragma: no cover
            raise ImportError(
                "DuckDBBackend requires duckdb. Install it with: pip install duckdb"
            ) from exc
        return duckdb.connect()

    def _check(self, data: Any) -> pd.DataFrame:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("DuckDBBackend expects a pandas DataFrame")
        return data

    def _query_scalar(self, data: pd.DataFrame, sql: str):
        con = self._connect()
        try:
            con.register("data", data)
            return con.execute(sql).fetchone()[0]
        finally:
            con.close()

    def num_rows(self, data: Any) -> int:
        return int(self._query_scalar(self._check(data), "SELECT COUNT(*) FROM data"))

    def get_column(self, data: Any, column: str) -> pd.Series:
        df = self._check(data)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found")
        return df[column]

    def count_nulls(self, data: Any, column: str) -> int:
        df = self._check(data)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found")
        return int(self._query_scalar(df, f'SELECT COUNT(*) FROM data WHERE "{column}" IS NULL'))

    def count_unique(self, data: Any, column: str) -> int:
        df = self._check(data)
        if column not in df.columns:
            raise KeyError(f"Column '{column}' not found")
        return int(self._query_scalar(df, f'SELECT COUNT(DISTINCT "{column}") FROM data'))
