import pandas as pd
import pytest


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 4],            # last two duplicate
            "email": ["a@x.com", "bad", "c@y.org", None, "d@z.io"],
            "age": [25, 17, 40, 200, None],   # 17 below, 200 above
            "status": ["active", "active", "banned", "unknown", "active"],
        }
    )
