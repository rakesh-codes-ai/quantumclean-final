import pandas as pd
from quantumclean import StatisticalOutlierDetector


def test_zscore_detects_outlier():
    df = pd.DataFrame({"v": [10, 11, 9, 10, 12, 1000]})
    r = StatisticalOutlierDetector("v", method="zscore", threshold=2).detect(df)
    assert 5 in r.anomaly_indices
    assert r.anomaly_count >= 1


def test_iqr_method():
    df = pd.DataFrame({"v": [1, 2, 3, 4, 5, 200]})
    r = StatisticalOutlierDetector("v", method="iqr").detect(df)
    assert 5 in r.anomaly_indices


def test_no_outliers_clean_data():
    df = pd.DataFrame({"v": [5, 5, 5, 5, 5]})
    r = StatisticalOutlierDetector("v").detect(df)
    assert r.anomaly_count == 0


def test_anomaly_rate():
    df = pd.DataFrame({"v": [1, 1, 1, 1, 999]})
    r = StatisticalOutlierDetector("v", threshold=1.5).detect(df)
    assert 0 <= r.anomaly_rate <= 1
