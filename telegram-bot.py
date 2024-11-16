import datetime as dt

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning


from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from constants import TOKEN
import os
import pandas as pd


filterwarnings(
    action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
)

START_ROUTES, END_ROUTES = range(2)
COUNTRIES, OTHER, PHONE_NUMBER, END = ["Countries", "Other", "Phone Number", "End"]


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
        df.to_csv("users_data (development).csv", index=False)
    df = pd.read_csv("users_data (development).csv")
    if user_id not in set(df["User Id"].values):
        df = pd.concat(
            [
                df,
                pd.DataFrame(
                    [[timestamp, user_id, username, first_name, last_name]],
                    columns=index_columns[:5],
                ),
            ]
        )
        df.to_csv("users_data (development).csv", index=False)
        df.to_excel("users_data.xlsx", index=False)

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


async def phone_number(update, context):
    query = update.callback_query
    await query.answer()
    message = query.message
    await message.reply_text(message)
    bot = context.bot
    chat_id = message.chat.id

    await query.message.reply_text(message.chat)

    # if message.contact:
    #     cpn = message.contact.phone_number
    #     cfn = message.contact.first_name
    #     await bot.send_message(chat_id, "#contact [{0}](https://telegram.me/{1})".format(user_id, username), parse_mode="Markdown", disable_web_page_preview=True)
    #     await bot.send_contact(chat_id,  phone_number=cpn, first_name=cfn)
    # if message.location:
    #     await bot.send_message(chat_id, "#location [{0}](https://telegram.me/{1})".format(user_id, username), parse_mode="Markdown", disable_web_page_preview=True)
    #     await bot.send_location(chat_id,  message.location.latitude, message.location.longitude)

    await bot.send_photo(chat_id, "ONE.jpg", "ONE image")

    # reply_markup = InlineKeyboardMarkup(
    #     [
    #         [
    #             InlineKeyboardButton("Phone Number", callback_data=str(THREE)),
    #             InlineKeyboardButton("Location", callback_data=str(FOUR)),
    #         ]
    #     ]
    # )
    # await message.reply_text(
    #     text="What do you want to send?", reply_markup=reply_markup
    # )
    return END_ROUTES


async def countries(update, context):
    query = update.callback_query
    await query.answer()
    message = query.message
    data = query.data
    match data:
        case "USA":
            await message.reply_text("Fuck USA")
        case "Viet Nam":
            df = pd.read_excel("users_data.xlsx")
            print(df)
            df.at[df.index[-1], "Country"] = data
            df.to_excel("users_data.xlsx", index=False)
        case "Other":
            await message.reply_text("👇 Please enter your country name below")
            return OTHER


async def loc_usa(update, context):
    await update.message.reply_text("Fuck USA")
    return END_ROUTES


async def loc_vietnam(update, context):
    df = pd.read_excel("user_info")
    print(pd)
    df.iloc[-1, "Country"] = "Viet Nam"


async def loc_other(update, context):
    query = update.callback_query
    await query.answer()
    message = query.message
    await message.reply_text("👇 Please enter your country name below")
    return OTHER


async def loc_other_specify(update, context):
    user_input = update.message.text
    await update.message.reply_text(user_input)
    df = pd.read_excel("users_data.xlsx")
    df.at[df.index[-1], "Country"] = update.message.text
    df.to_excel("users_data.xlsx", index=False)
    # await update.message.reply_text(f"Your country has been set to {user_input}")
    # return END_ROUTES


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
            OTHER: [MessageHandler(filters.TEXT, loc_other_specify)],
            END_ROUTES: [
                CallbackQueryHandler(end, pattern="^" + str(END) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
