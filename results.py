"""
CASE STUDY 1 — Customer records validation
==========================================
Scenario: a company imports a customer CSV and must reject bad rows before
loading them into a CRM. Demonstrates the Sprint 1 validation engine on a
realistic, messy dataset generated in-code (no download needed).
"""
import pandas as pd
from quantumclean import (
    Schema, NotNullValidator, UniqueValidator, EmailValidator,
    RangeValidator, CategoricalValidator,
)

customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104, 104, 106],   # 104 duplicated
    "email":       ["ann@shop.com", "invalid-email", "cara@shop.com",
                    None, "dan@shop.com", "eve@shop.com"],
    "age":         [34, 28, 150, 41, 29, 22],         # 150 impossible
    "tier":        ["gold", "silver", "bronze", "platinum", "gold", "silver"],
})

schema = (
    Schema()
    .add(NotNullValidator("customer_id"))
    .add(UniqueValidator("customer_id"))
    .add(EmailValidator("email", allow_null=False))
    .add(RangeValidator("age", min_value=18, max_value=120))
    .add(CategoricalValidator("tier", ["gold", "silver", "bronze"]))
)

result = schema.validate(customers)
print("CASE STUDY 1 — Customer validation")
print(result.summary())
print("\nRows to reject per rule:")
for r in result.failures():
    print(f"  {r.validator:<12} -> rows {r.failed_indices}")
