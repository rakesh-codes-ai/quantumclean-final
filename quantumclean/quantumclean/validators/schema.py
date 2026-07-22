"""Schema: a composable collection of validators run as one unit."""
from __future__ import annotations

from typing import Iterable, List, Optional

import pandas as pd

from .results import SchemaResult
from .validators.base import BaseValidator


class Schema:
    """Group validators and run them together against a DataFrame.

    Supports a fluent (chainable) ``add`` API:

        schema = (
            Schema()
            .add(NotNullValidator("id"))
            .add(UniqueValidator("id"))
            .add(EmailValidator("email"))
        )
        result = schema.validate(df)
    """

    def __init__(self, validators: Optional[Iterable[BaseValidator]] = None):
        self._validators: List[BaseValidator] = []
        if validators:
            for v in validators:
                self.add(v)

    def add(self, validator: BaseValidator) -> "Schema":
        if not isinstance(validator, BaseValidator):
            raise TypeError("validator must be a BaseValidator instance")
        self._validators.append(validator)
        return self

    @property
    def validators(self) -> List[BaseValidator]:
        return list(self._validators)

    def validate(self, df: pd.DataFrame) -> SchemaResult:
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")
        results = [v.validate(df) for v in self._validators]
        return SchemaResult(results=results)

    def __len__(self) -> int:
        return len(self._validators)

    def __repr__(self) -> str:
        return f"<Schema with {len(self._validators)} validator(s)>"
