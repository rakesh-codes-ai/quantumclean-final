import pandas as pd
from quantumclean import NotNullValidator


def test_all_present():
    df = pd.DataFrame({"x": [1, 2, 3]})
    r = NotNullValidator("x").validate(df)
    assert r.is_valid
    assert r.passed == 3 and r.failed == 0


def test_detects_nulls(sample_df):
    r = NotNullValidator("email").validate(sample_df)
    assert not r.is_valid
    assert r.failed == 1
    assert 3 in r.failed_indices


def test_pass_rate(sample_df):
    r = NotNullValidator("age").validate(sample_df)
    assert r.pass_rate == 0.8
