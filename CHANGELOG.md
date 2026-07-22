import pandas as pd
from quantumclean import QualityScorer, Schema, NotNullValidator, EmailValidator


def test_perfect_data_scores_high():
    df = pd.DataFrame({"id": [1, 2, 3], "name": ["a", "b", "c"]})
    score = QualityScorer().score(df)
    assert score.completeness == 1.0
    assert score.overall > 0.9


def test_missing_values_lower_completeness():
    df = pd.DataFrame({"x": [1, None, None, 4]})
    score = QualityScorer().score(df)
    assert score.completeness == 0.5


def test_validity_uses_schema():
    df = pd.DataFrame({"email": ["a@x.com", "bad", "c@y.com"]})
    schema = Schema([EmailValidator("email")])
    score = QualityScorer().score(df, schema=schema)
    assert score.validity < 1.0


def test_summary_and_dict():
    df = pd.DataFrame({"id": [1, 2, 3]})
    score = QualityScorer().score(df)
    assert "OVERALL" in score.summary()
    assert "overall" in score.to_dict()


def test_custom_weights():
    df = pd.DataFrame({"x": [1, None]})
    score = QualityScorer(weights={"completeness": 4, "uniqueness": 0,
                                   "validity": 0, "consistency": 0}).score(df)
    assert round(score.overall, 3) == round(score.completeness, 3)
