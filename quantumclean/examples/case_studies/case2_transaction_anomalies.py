"""
CASE STUDY 2 — Transaction anomaly detection
============================================
Scenario: a payments team screens transactions for suspicious amounts.
Demonstrates the Sprint 2 anomaly detectors (statistical + machine learning).
"""
import pandas as pd
from quantumclean import StatisticalOutlierDetector, IsolationForestDetector

transactions = pd.DataFrame({
    "txn_id": range(1, 13),
    "amount": [50, 55, 48, 60, 52, 47, 51, 9999, 49, 53, 58, 12000],  # 2 frauds
})

print("CASE STUDY 2 — Transaction anomaly detection\n")

zscore = StatisticalOutlierDetector("amount", method="zscore", threshold=2.5).detect(transactions)
print("Statistical (z-score):", zscore)
print("  flagged rows:", zscore.anomaly_indices)

iforest = IsolationForestDetector("amount", contamination=0.2).detect(transactions)
print("\nMachine learning (Isolation Forest):", iforest)
print("  flagged rows:", iforest.anomaly_indices)
