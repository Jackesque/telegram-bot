import pandas as pd

from utils.constants import USERS_DATA_COLUMNS, USERS_DATA_PATH


def update_user_data(user_id, data):
    try:
        df = pd.read_excel(USERS_DATA_PATH)
    except FileNotFoundError:
        df = pd.DataFrame(columns=USERS_DATA_COLUMNS)

    if user_id in df["User ID"].values:
        user_row = pd.DataFrame(df.loc[df["User ID"] == user_id])

        data_to_update = {
            key: value for key, value in data.items() if key != "Timestamp"
        }
        for key, value in data_to_update.items():
            df.loc[user_row.index, key] = value
    else:
        df = pd.concat(
            [df, pd.DataFrame([{"User ID": user_id, **data}])], ignore_index=True
        )
    df = df.fillna("")
    df.to_excel(USERS_DATA_PATH, index=False)
