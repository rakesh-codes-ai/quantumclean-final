import pandas as pd
import pytest
from quantumclean import get_backend, PandasBackend


def test_factory_returns_pandas():
    assert isinstance(get_backend("pandas"), PandasBackend)


def test_unknown_backend_raises():
    with pytest.raises(ValueError):
        get_backend("snowflake")


def test_pandas_backend_ops():
    df = pd.DataFrame({"id": [1, 2, 2, None]})
    b = get_backend()
    assert b.num_rows(df) == 4
    assert b.count_nulls(df, "id") == 1
    assert b.count_unique(df, "id") == 2


def test_missing_column_raises():
    b = get_backend()
    with pytest.raises(KeyError):
        b.get_column(pd.DataFrame({"a": [1]}), "b")
