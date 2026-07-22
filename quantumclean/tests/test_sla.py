import pandas as pd
import pytest
from quantumclean import QualitySLA, QualityScorer


def _score(df):
    return QualityScorer().score(df)


def test_requires_at_least_one_threshold():
    with pytest.raises(ValueError):
        QualitySLA()


def test_threshold_must_be_fraction():
    with pytest.raises(ValueError):
        QualitySLA(min_overall=1.5)


def test_sla_met():
    score = _score(pd.DataFrame({"id": [1, 2, 3]}))
    report = QualitySLA(min_overall=0.5, min_completeness=0.9).check(score)
    assert report.is_met
    assert report.breaches == []


def test_sla_breached():
    score = _score(pd.DataFrame({"x": [1, None, None, None]}))  # completeness 0.25
    report = QualitySLA(min_completeness=0.9).check(score)
    assert not report.is_met
    assert report.breaches[0].metric == "completeness"
    assert report.breaches[0].actual < 0.9


def test_summary_text():
    score = _score(pd.DataFrame({"id": [1, 2]}))
    report = QualitySLA(min_overall=0.1).check(score)
    assert "SLA" in report.summary()


def test_check_rejects_non_score():
    with pytest.raises(TypeError):
        QualitySLA(min_overall=0.5).check("not a score")
