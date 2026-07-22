"""Sprint 3 demo: data lineage + Quality SLA + multi-backend (DuckDB)."""
import pandas as pd

from quantumclean import (
    Schema, NotNullValidator, EmailValidator, RangeValidator,
    QualityScorer, QualitySLA, LineageTracker, get_backend,
)

# --- A small "pipeline" with messy data -------------------------------
df = pd.DataFrame({
    "user_id": [1, 2, 3, 4, 5],
    "email": ["a@x.com", "bad-email", "c@y.org", None, "e@w.com"],
    "age": [25, 31, 29, 27, 30],
})

print("=== 1. Data lineage (the dataset's diary) ===")
lineage = (
    LineageTracker("users_dataset")
    .add_source("users.csv")
    .record("loaded", rows=len(df))
    .record("validated", schema="user_schema")
)
print(lineage.summary())

print("\n=== 2. Quality score ===")
schema = Schema([
    NotNullValidator("user_id"),
    EmailValidator("email", allow_null=False),
    RangeValidator("age", min_value=0, max_value=120),
])
score = QualityScorer().score(df, schema=schema)
print(score.summary())

print("\n=== 3. Quality SLA enforcement ===")
strict = QualitySLA(min_overall=0.95, min_completeness=0.99)
print(strict.check(score).summary())          # expected: BREACHED
relaxed = QualitySLA(min_overall=0.80)
print()
print(relaxed.check(score).summary())         # expected: MET

print("\n=== 4. Same API, different engines ===")
for name in ("pandas", "duckdb"):
    b = get_backend(name)
    print(f"[{b.name:6}] rows={b.num_rows(df)}  "
          f"null emails={b.count_nulls(df, 'email')}  "
          f"unique ids={b.count_unique(df, 'user_id')}")
