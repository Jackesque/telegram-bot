import pandas as pd
import os

df = pd.concat(
    [
        pd.DataFrame(
            [[1, 2, 3, 4, 5]],
            columns=["User Id", "Username", "First Name", "Last Name", "Timestamp"],
        ),
        pd.DataFrame(
            [[6, 7]],
            columns=["User Id", "Username"],
        ),
    ]
)
df.iloc[-1, 2:] = ["First", "Last", "2023-10-01"]
print(df)