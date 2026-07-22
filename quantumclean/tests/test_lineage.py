import pytest
from quantumclean import LineageTracker


def test_requires_name():
    with pytest.raises(ValueError):
        LineageTracker("")


def test_add_source_and_record_chain():
    t = (
        LineageTracker("users_dataset")
        .add_source("users.csv")
        .record("dropped_duplicates", rows_removed=2)
        .record("validated", schema="user_schema")
    )
    assert t.sources == ["users.csv"]
    assert len(t.events) == 3  # source_added + 2 operations


def test_to_dict_structure():
    t = LineageTracker("d").add_source("a.csv").record("cleaned")
    d = t.to_dict()
    assert d["dataset"] == "d"
    assert d["sources"] == ["a.csv"]
    assert d["events"][1]["operation"] == "cleaned"


def test_summary_contains_name_and_ops():
    t = LineageTracker("sales").add_source("sales.csv").record("normalized")
    s = t.summary()
    assert "sales" in s and "normalized" in s


def test_empty_operation_raises():
    with pytest.raises(ValueError):
        LineageTracker("d").record("")
