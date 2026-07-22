"""Smoke tests that each case study runs end-to-end without error."""
import runpy
import os
import pytest

HERE = os.path.dirname(__file__)
CASES = os.path.join(HERE, "..", "examples", "case_studies")

# Map each case study to any optional dependency it needs, so the test
# skips cleanly (instead of erroring) when that library isn't installed.
_REQUIRES = {
    "case1_customer_validation.py": [],
    "case2_transaction_anomalies.py": ["sklearn"],
    "case3_pipeline_governance.py": ["duckdb"],
}


@pytest.mark.parametrize("script", list(_REQUIRES))
def test_case_study_runs(script):
    for module in _REQUIRES[script]:
        pytest.importorskip(module)
    path = os.path.join(CASES, script)
    # runs the whole script; any exception fails the test
    runpy.run_path(path, run_name="__main__")
