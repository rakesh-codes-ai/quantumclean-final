"""Sprint 2 demo: anomaly detection + quality scoring + backend."""
import pandas as pd

from quantumclean import (
    Schema, NotNullValidator, EmailValidator, RangeValidator,
    StatisticalOutlierDetector, IsolationForestDetector,
    QualityScorer, get_backend,
)

df = pd.DataFrame({
    "user_id": [1, 2, 3, 4, 5, 6],
    "email": ["a@x.com", "bad", "c@y.org", "d@z.io", "e@w.com", None],
    "age": [25, 31, 29, 27, 30, 900],          # 900 is an outlier
    "salary": [50000, 52000, 51000, 49000, 50500, 999999],  # outlier
})

print("=== 1. Anomaly Detection (statistical) ===")
res = StatisticalOutlierDetector("age", method="zscore", threshold=2).detect(df)
print(res, "-> rows", res.anomaly_indices)

print("\n=== 2. Anomaly Detection (Isolation Forest / ML) ===")
res2 = IsolationForestDetector("salary", contamination=0.2).detect(df)
print(res2, "-> rows", res2.anomaly_indices)

print("\n=== 3. Quality Score ===")
schema = Schema([NotNullValidator("user_id"), EmailValidator("email"),
                 RangeValidator("age", min_value=0, max_value=120)])
score = QualityScorer().score(df, schema=schema)
print(score.summary())

print("\n=== 4. Backend abstraction ===")
backend = get_backend("pandas")
print(f"Backend: {backend.name}, rows: {backend.num_rows(df)}, "
      f"unique user_ids: {backend.count_unique(df, 'user_id')}")
