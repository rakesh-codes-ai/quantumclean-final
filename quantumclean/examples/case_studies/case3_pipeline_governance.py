"""
CASE STUDY 3 — End-to-end pipeline governance
==============================================
Scenario: a data platform team runs a nightly pipeline and must PROVE quality
(score + SLA) and PROVENANCE (lineage) for auditors. Ties together Sprint 2
scoring, Sprint 3 SLA + lineage, across two interchangeable backends.
"""
import pandas as pd
from quantumclean import (
    Schema, NotNullValidator, EmailValidator, RangeValidator,
    QualityScorer, QualitySLA, LineageTracker, get_backend,
)

data = pd.DataFrame({
    "user_id": [1, 2, 3, 4, 5],
    "email":   ["a@x.com", "bad", "c@y.org", None, "e@w.com"],
    "age":     [25, 33, 29, 41, 27],
})

# 1. Provenance
lineage = (LineageTracker("nightly_users")
           .add_source("s3://raw/users.csv")
           .record("loaded", rows=len(data))
           .record("deduplicated"))

# 2. Score
schema = Schema([NotNullValidator("user_id"),
                 EmailValidator("email", allow_null=False),
                 RangeValidator("age", min_value=18, max_value=120)])
score = QualityScorer().score(data, schema=schema)

# 3. Enforce contract
sla = QualitySLA(min_overall=0.90, min_completeness=0.95)
report = sla.check(score)

print("CASE STUDY 3 — Pipeline governance\n")
print(lineage.summary())
print("\n" + score.summary())
print("\n" + report.summary())
print("\nBackend cross-check (same answers, different engines):")
for engine in ("pandas", "duckdb"):
    b = get_backend(engine)
    print(f"  [{engine:6}] rows={b.num_rows(data)} unique_ids={b.count_unique(data,'user_id')}")

print(f"\nPIPELINE DECISION: {'PASS - load to warehouse' if report.is_met else 'FAIL - quarantine batch'}")
