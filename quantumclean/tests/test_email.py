import pandas as pd
import pytest
from quantumclean import EmailValidator


def test_valid_and_invalid(sample_df):
    r = EmailValidator("email").validate(sample_df)
    # "bad" fails; null allowed by default
    assert r.failed == 1
    assert 1 in r.failed_indices


def test_null_disallowed(sample_df):
    r = EmailValidator("email", allow_null=False).validate(sample_df)
    assert r.failed == 2          # "bad" + null
    assert set(r.failed_indices) == {1, 3}


def test_missing_column_raises(sample_df):
    with pytest.raises(KeyError):
        EmailValidator("nope").validate(sample_df)


def test_empty_column_name_raises():
    with pytest.raises(ValueError):
        EmailValidator("")
