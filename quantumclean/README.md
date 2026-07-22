# QuantumClean

[![CI](https://github.com/<your-org>/quantumclean/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-org>/quantumclean/actions)
![coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![python](https://img.shields.io/badge/python-3.8%2B-blue)
![version](https://img.shields.io/badge/version-1.0.0-success)

A production-grade, extensible **data quality library** for data engineers.
Define quality rules once, run them anywhere in your pipeline, and get a
clear pass/fail report with the exact rows that failed.

> Capstone Project — INFO-6156 | Devansh, Darshan, Rakesh Manimaran

## Why QuantumClean

Data quality rules get copy-pasted across projects and break when data grows.
QuantumClean packages those rules into reusable validators with a single,
consistent API, designed to scale from a local DataFrame to distributed
backends (Spark, DuckDB) in later releases.

## Install (development)

```bash
git clone https://github.com/<your-org>/quantumclean.git
cd quantumclean
pip install -e ".[dev]"
```

## Quick start

```python
import pandas as pd
from quantumclean import (
    Schema, NotNullValidator, UniqueValidator,
    EmailValidator, RangeValidator, CategoricalValidator,
)

df = pd.read_csv("users.csv")

schema = (
    Schema()
    .add(NotNullValidator("user_id"))
    .add(UniqueValidator("user_id"))
    .add(EmailValidator("email"))
    .add(RangeValidator("age", min_value=18, max_value=120))
    .add(CategoricalValidator("status", ["active", "banned"]))
)

result = schema.validate(df)
print(result.summary())          # human-readable report
print(result.to_dict())          # machine-readable for dashboards/SLAs
```

## Built-in validators (v0.1.0)

| Validator              | Checks                                  |
| ---------------------- | --------------------------------------- |
| `NotNullValidator`     | No missing values                       |
| `UniqueValidator`      | No duplicate values                     |
| `EmailValidator`       | Valid email format                      |
| `RangeValidator`       | Numeric within min/max bounds           |
| `RegexValidator`       | Matches a custom pattern                |
| `CategoricalValidator` | Value is in an allowed set              |

## Custom validators

Subclass `BaseValidator` and implement one method — no core changes needed:

```python
from quantumclean import BaseValidator

class PositiveValidator(BaseValidator):
    name = "positive"
    def _validate_series(self, series):
        return series.fillna(0) > 0
```

## Roadmap

- v0.2 — Anomaly detection (statistical + Isolation Forest), multi-metric quality scoring, backend abstraction + Pandas backend ✅ **(Sprint 2 complete)**
- v0.3 — Data lineage tracking, Quality SLA enforcement, DuckDB + Spark backends ✅ **(Sprint 3 complete)**
- v0.4 — (folded into 1.0)
- **v1.0 — Case studies, full docs, automated release pipeline, PyPI-ready ✅ (Sprint 4 complete)**

## Case studies

Three runnable, real-world examples live in `examples/case_studies/`:
1. `case1_customer_validation.py` — reject bad customer rows before a CRM import.
2. `case2_transaction_anomalies.py` — flag suspicious payment amounts (statistical + ML).
3. `case3_pipeline_governance.py` — score, enforce an SLA, and track lineage across backends.

Run any of them, e.g.: `python examples/case_studies/case3_pipeline_governance.py`

## Development

```bash
pytest                 # run tests with coverage
```

## License

MIT — see [LICENSE](LICENSE).
