import pandas as pd
import pytest
from quantumclean import CategoricalValidator


def test_allowed_values(sample_df):
    r = CategoricalValidator("status", ["active", "banned"]).validate(sample_df)
    assert set(r.failed_indices) == {3}   # "unknown"


def test_empty_categories_raises():
    with pytest.raises(ValueError):
        CategoricalValidator("status", [])
