"""Backend abstraction: one interface, many execution engines.

Sprint 2 ships the Pandas backend. Later sprints add Spark and DuckDB
backends that implement this same interface, so the rest of the library
never needs to know which engine is running underneath.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseBackend(ABC):
    name: str = "base"

    @abstractmethod
    def num_rows(self, data: Any) -> int: ...

    @abstractmethod
    def get_column(self, data: Any, column: str) -> Any: ...

    @abstractmethod
    def count_nulls(self, data: Any, column: str) -> int: ...

    @abstractmethod
    def count_unique(self, data: Any, column: str) -> int: ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}'>"
