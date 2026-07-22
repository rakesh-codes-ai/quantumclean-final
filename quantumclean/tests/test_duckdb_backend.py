import pandas as pd
import pytest

pytest.importorskip("duckdb")
from quantumclean import get_backend, DuckDBBackend


def test_factory_returns_duckdb():
    assert isinstance(get_backend("duckdb"), DuckDBBackend)


def test_ops_match_pandas():
    df = pd.DataFrame({"id": [1, 2, 2, None], "name": ["a", "b", "c", "d"]})
    b = get_backend("duckdb")
    assert b.num_rows(df) == 4
    assert b.count_nulls(df, "id") == 1
    assert b.count_unique(df, "id") == 2


def test_missing_column_raises():
    with pytest.raises(KeyError):
        get_backend("duckdb").count_nulls(pd.DataFrame({"a": [1]}), "b")


def test_rejects_non_dataframe():
    with pytest.raises(TypeError):
        get_backend("duckdb").num_rows([1, 2, 3])
