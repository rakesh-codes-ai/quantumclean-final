import pandas as pd
import pytest
from quantumclean import RangeValidator


def test_min_and_max(sample_df):
    r = RangeValidator("age", min_value=18, max_value=120).validate(sample_df)
    # 17 (idx1) and 200 (idx3) fail; null (idx4) allowed
    assert set(r.failed_indices) == {1, 3}


def test_exclusive_bounds():
    df = pd.DataFrame({"v": [0, 5, 10]})
    r = RangeValidator("v", min_value=0, max_value=10, inclusive=False).validate(df)
    assert set(r.failed_indices) == {0, 2}


def test_requires_a_bound():
    with pytest.raises(ValueError):
        RangeValidator("v")


def test_non_numeric_fails():
    df = pd.DataFrame({"v": ["abc", "5", "9"]})
    r = RangeValidator("v", min_value=0, max_value=10).validate(df)
    assert 0 in r.failed_indices
