import pandas as pd
import pytest
from quantumclean import (
    Schema, NotNullValidator, UniqueValidator,
    EmailValidator, RangeValidator, CategoricalValidator,
)


def test_schema_runs_all(sample_df):
    schema = (
        Schema()
        .add(NotNullValidator("id"))
        .add(UniqueValidator("id"))
        .add(EmailValidator("email"))
        .add(RangeValidator("age", min_value=18, max_value=120))
        .add(CategoricalValidator("status", ["active", "banned"]))
    )
    result = schema.validate(sample_df)
    assert len(schema) == 5
    assert not result.is_valid
    assert len(result.failures()) == 4   # id-unique, email, range, categorical
    assert 0.0 <= result.pass_rate <= 1.0


def test_schema_summary_and_dict(sample_df):
    schema = Schema([NotNullValidator("id")])
    result = schema.validate(sample_df)
    assert result.is_valid
    assert "Schema validation" in result.summary()
    d = result.to_dict()
    assert d["is_valid"] is True
    assert d["results"][0]["validator"] == "not_null"


def test_schema_rejects_bad_validator():
    with pytest.raises(TypeError):
        Schema().add("not a validator")


def test_schema_rejects_non_dataframe():
    with pytest.raises(TypeError):
        Schema([NotNullValidator("id")]).validate([1, 2, 3])


def test_empty_schema_is_valid():
    assert Schema().validate(pd.DataFrame({"x": [1]})).is_valid
