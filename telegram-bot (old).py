import datetime as dt
import os
from warnings import filterwarnings

import pandas as pd
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.warnings import PTBUserWarning

from utils.constants import TOKEN, USERS_DATA_PATH

filterwarnings(
    action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
)

START_ROUTES, END_ROUTES = range(2)
COUNTRIES, COUNTRIES_OTHER, PHONE_NUMBER, END = [
    "Countries",
    "Other",
    "Phone Number",
    "End",
]

print("Bot started...")


async def start(update, context):
    message = update.message
    user = message.from_user
    timestamp = (message.date + dt.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
    user_id = str(user.id)
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    file_exists = os.path.exists(os.path.join(os.getcwd(), "user_info.xlsx"))
    index_columns = [
        "Timestamp",
        "User Id",
        "Username",
        "First Name",
        "Last Name",
        "Phone Number",
        "Broker UID",
        "Broker Full Name",
        "Country",
        "Account Balance (USD)",
        "Email (for VIP invitation)",
    ]
    if not file_exists:
        df = pd.DataFrame(columns=index_columns)
        df.to_excel(USERS_DATA_PATH, index=False)
    if user_id not in set(str(df["User Id"].values)):
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [[timestamp, user_id, username, first_name, last_name]],
                    columns=index_columns[:5],
                ),
            ]
        )
        # df.to_csv("users_data (development).csv", index=False)
        df.to_excel(USERS_DATA_PATH, index=False)

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Viet Nam", callback_data="Viet Nam"),
                InlineKeyboardButton("USA", callback_data="USA"),
                InlineKeyboardButton("Other", callback_data="Other"),
            ]
        ]
    )
    await message.reply_text(text="What is your country?", reply_markup=reply_markup)
    return COUNTRIES


async def countries(update, context):
    query = update.callback_query
    await query.answer()
    message = query.message
    user_text = query.data
    match user_text:
        case "USA":
            await message.reply_text("Fuck USA")
        case "Viet Nam":
            df = pd.read_excel(USERS_DATA_PATH)
            df.at[df.index[-1], "Country"] = user_text
            df.to_excel(USERS_DATA_PATH, index=False)
            await message.reply_text(
                "That's so great to hear. I'm from Viet Nam, too.\n\n👇 Please enter your phone number below"
            )
        case "Other":
            await message.reply_text("👇 Please enter your country name below")
            return COUNTRIES_OTHER

    return PHONE_NUMBER


async def countries_other(update, context):
    message = update.message
    user_text = message.text
    df = pd.read_excel(USERS_DATA_PATH)
    df.at[df.index[-1], "Country"] = user_text
    df.to_excel(USERS_DATA_PATH, index=False)
    await message.reply_text(
        f"{user_text} is a nice country. I've heard great things about it!\n\n👇 Please enter your phone number below",
    )

    return PHONE_NUMBER


async def phone_number(update, context):
    message = update.message
    user_text = message.text
    df = pd.read_excel(USERS_DATA_PATH)
    df.at[df.index[-1], "Phone Number"] = user_text
    df.to_excel(USERS_DATA_PATH, index=False)
    await message.reply_text("I have received your information.")

    # bot = context.bot
    # chat_id = message.chat.id
    # await bot.send_photo(chat_id, "ONE.jpg", "ONE image")
    return END_ROUTES


async def not_phone_number(update, context):
    await update.message.reply_text(
        "Seems like you entered an invalid phone number. Please enter again."
    )

    return PHONE_NUMBER


async def end(update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(text="See you next time!")
    return ConversationHandler.END


def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            COUNTRIES: [
                CallbackQueryHandler(countries, pattern=""),
            ],
            # https://github.com/bulv1ne/country_list/ filters.Text(country_list)
            COUNTRIES_OTHER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, countries_other)
            ],
            PHONE_NUMBER: [
                MessageHandler(filters.Regex(r"\d{10,11}"), phone_number),
                MessageHandler(filters.TEXT & ~filters.COMMAND, not_phone_number),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
