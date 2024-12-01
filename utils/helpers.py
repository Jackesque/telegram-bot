import os

import pandas as pd

from utils.constants import (
    USERS_DATA_COLUMNS,
    USERS_DATA_COLUMNS_VI,
    USERS_DATA_PATH,
    USERS_DATA_PATH_VI,
)


def update_user_data(user_id, data, language="vi"):
    match language:
        case "vi":
            users_data_path = USERS_DATA_PATH_VI
            users_data_columns = USERS_DATA_COLUMNS_VI
            user_id_column_name = "Id người dùng"
            timestamp_column_name = "Thời gian"
        case "en" | _:
            users_data_path = USERS_DATA_PATH
            users_data_columns = USERS_DATA_COLUMNS
            user_id_column_name = "User Id"
            timestamp_column_name = "Timestamp"
    try:
        df = pd.read_excel(users_data_path, dtype=str)
    except FileNotFoundError:
        df = pd.DataFrame(columns=users_data_columns)

    if user_id in df[user_id_column_name].array:
        user_row = pd.DataFrame(df.loc[df[user_id_column_name] == user_id])

        data_to_update = {
            key: value
            for key, value in data.items()
            if key not in [timestamp_column_name, user_id_column_name]
        }
        for key, value in data_to_update.items():
            df.loc[user_row.index, key] = value
    else:
        df = pd.concat(
            [df, pd.DataFrame([{user_id_column_name: user_id, **data}])],
            ignore_index=True,
        )
    df.to_excel(users_data_path, index=False)


async def send_bulk_images(bot, chat_id, directory_path, caption=""):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
            with open(os.path.join(directory_path, filename), "rb") as image_file:
                caption = (
                    os.path.splitext(filename)[0] if caption.strip() == "" else caption
                )
                await bot.send_photo(chat_id, image_file)
