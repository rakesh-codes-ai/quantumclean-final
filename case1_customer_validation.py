"""Minimal end-to-end example of QuantumClean."""
import pandas as pd

from quantumclean import (
    Schema,
    NotNullValidator,
    UniqueValidator,
    EmailValidator,
    RangeValidator,
    CategoricalValidator,
)

df = pd.DataFrame(
    {
        "user_id": [1, 2, 3, 3],
        "email": ["a@x.com", "not-an-email", "c@y.org", "d@z.io"],
        "age": [25, 17, 41, 30],
        "status": ["active", "active", "frozen", "active"],
    }
)

schema = (
    Schema()
    .add(NotNullValidator("user_id"))
    .add(UniqueValidator("user_id"))
    .add(EmailValidator("email"))
    .add(RangeValidator("age", min_value=18, max_value=120))
    .add(CategoricalValidator("status", ["active", "banned"]))
)

result = schema.validate(df)
print(result.summary())
print("\nFailed rows per validator:")
for r in result.failures():
    print(f"  {r.validator} -> rows {r.failed_indices}")
