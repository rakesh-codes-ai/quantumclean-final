import pandas as pd
import pytest
from quantumclean import get_backend, SparkBackend

try:
    import pyspark  # noqa: F401
    HAS_SPARK = True
except ImportError:
    HAS_SPARK = False


def test_factory_returns_spark():
    assert isinstance(get_backend("spark"), SparkBackend)
    assert get_backend("spark").name == "spark"


@pytest.mark.skipif(HAS_SPARK, reason="pyspark installed; error path not applicable")
def test_clear_error_without_pyspark():
    with pytest.raises(ImportError):
        get_backend("spark").num_rows(pd.DataFrame({"a": [1]}))
