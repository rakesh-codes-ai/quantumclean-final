import pandas as pd
from quantumclean import RegexValidator


def test_pattern_match():
    df = pd.DataFrame({"code": ["AB12", "abc", "ZZ99"]})
    r = RegexValidator("code", r"^[A-Z]{2}[0-9]{2}$").validate(df)
    assert set(r.failed_indices) == {1}


def test_null_allowed_by_default():
    df = pd.DataFrame({"code": ["AB12", None]})
    r = RegexValidator("code", r"^[A-Z]{2}[0-9]{2}$").validate(df)
    assert r.is_valid
