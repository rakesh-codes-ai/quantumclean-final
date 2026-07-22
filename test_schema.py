import pandas as pd
from quantumclean import UniqueValidator


def test_duplicates_flagged(sample_df):
    r = UniqueValidator("id").validate(sample_df)
    # both rows holding the value 4 are flagged
    assert set(r.failed_indices) == {3, 4}


def test_all_unique():
    df = pd.DataFrame({"id": [1, 2, 3]})
    assert UniqueValidator("id").validate(df).is_valid


def test_nulls_ignored_by_default():
    df = pd.DataFrame({"id": [1, None, None]})
    assert UniqueValidator("id").validate(df).is_valid
