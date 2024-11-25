import pandas as pd

from utils.constants import DEV_USERS_DATA_PATH, USERS_DATA_COLUMNS, USERS_DATA_PATH


def update_user_data(user_id, data):
    try:
        df = pd.read_csv(DEV_USERS_DATA_PATH)
    except FileNotFoundError:
        df = pd.DataFrame(columns=USERS_DATA_COLUMNS)

    if user_id in df["User Id"].array:
        user_row = pd.DataFrame(df.loc[df["User Id"] == user_id])

        data_to_update = {
            key: value
            for key, value in data.items()
            if key not in ["Timestamp", "User Id"]
        }
        for key, value in data_to_update.items():
            df.loc[user_row.index, key] = value
    else:
        df = pd.concat(
            [df, pd.DataFrame([{"User Id": user_id, **data}])], ignore_index=True
        )
    df = df.fillna("")
    df.to_csv(DEV_USERS_DATA_PATH, index=False)
    df.to_excel(USERS_DATA_PATH, index=False)
