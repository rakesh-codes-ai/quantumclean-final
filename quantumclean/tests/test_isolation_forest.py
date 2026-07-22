import pandas as pd
import pytest

pytest.importorskip("sklearn")
from quantumclean import IsolationForestDetector


def test_detects_anomaly():
    df = pd.DataFrame({"v": [10, 11, 10, 12, 9, 11, 500]})
    r = IsolationForestDetector("v", contamination=0.2).detect(df)
    assert r.anomaly_count >= 1
    assert 6 in r.anomaly_indices


def test_too_few_rows():
    df = pd.DataFrame({"v": [1]})
    r = IsolationForestDetector("v").detect(df)
    assert r.anomaly_count == 0
