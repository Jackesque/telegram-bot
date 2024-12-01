# import datetime as dt
# import re
# import subprocess
# from warnings import filterwarnings

# from telegram import (
#     InlineKeyboardButton,
#     InlineKeyboardMarkup,
#     ReplyKeyboardRemove,
#     Update,
# )
# from telegram.ext import (
#     Application,
#     CallbackContext,
#     CallbackQueryHandler,
#     CommandHandler,
#     ConversationHandler,
#     MessageHandler,
#     filters,
# )
# from telegram.warnings import PTBUserWarning

# from utils.constants import ACCOUNT_LINK, GUIDE_IMAGE_PATH, PLATFORMS_KEYBOARD, TOKEN
# from utils.helpers import update_user_data

# filterwarnings(
#     action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
# )

# subprocess.run(
#     ["pip", "install", "-r", "requirements.txt"],
#     capture_output=True,
#     text=True,
#     check=False,
# )

# print("Bot started...")
# SELECT_COUNTRY, ASK_COUNTRY_OTHER, ASK_PHONE, SELECT_PLATFORM, ASK_DEPOSIT = range(5)


# async def start(update: Update, context: CallbackContext) -> int:
#     message = update.message
#     user = update.effective_user
#     timestamp = (message.date + dt.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
#     user_data = {
#         "Timestamp": timestamp,
#         "User Id": str(user.id),
#         "Username": user.username,
#         "First Name": user.first_name,
#         "Last Name": user.last_name,
#     }
#     context.user_data["User Id"] = str(user.id)

#     update_user_data(context.user_data["User Id"], user_data)

#     reply_markup = InlineKeyboardMarkup(
#         [
#             [
#                 InlineKeyboardButton("Viet Nam", callback_data="Viet Nam"),
#                 InlineKeyboardButton("USA", callback_data="USA"),
#                 InlineKeyboardButton("Other", callback_data="Other"),
#             ]
#         ]
#     )
#     await message.reply_text("Which country are you from?", reply_markup=reply_markup)
#     return SELECT_COUNTRY


# async def select_country(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     await query.answer()
#     message = query.message
#     selected_country = query.data
#     update_user_data(context.user_data["User Id"], {"Country": selected_country})

#     if selected_country == "Viet Nam":
#         await message.reply_text(
#             "That's so great to hear. I'm from Viet Nam, too.\n\n👇 Please enter your phone number below"
#         )
#         return ASK_PHONE
#     elif selected_country == "USA":
#         await message.reply_text(
#             "Unfortunately, we do not support US residents at this time."
#         )
#         return ConversationHandler.END
#     elif selected_country == "Other":
#         await message.reply_text("👇 Please type your country name below")
#         return ASK_COUNTRY_OTHER


# async def ask_country_other(update: Update, context: CallbackContext) -> int:
#     message = update.message
#     typed_country = message.text
#     update_user_data(context.user_data["User Id"], {"Country": typed_country})

#     await message.reply_text(
#         f"{typed_country} is a nice country. I've heard great things about it!\n\n👇 What is your phone number?"
#     )
#     return ASK_PHONE


# async def ask_phone(update: Update, context: CallbackContext) -> int:
#     message = update.message
#     phone = message.text

#     if not re.fullmatch(r"\d{10,11}", phone):
#         await message.reply_text(
#             "Seems like you typed an invalid phone number. Please type again"
#         )
#         return ASK_PHONE

#     update_user_data(context.user_data["User Id"], {"Phone": str(phone)})
#     await message.reply_text(
#         "Which trading platform are you using?", reply_markup=PLATFORMS_KEYBOARD
#     )
#     return SELECT_PLATFORM


# async def select_platform(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     await query.answer()
#     message = query.message
#     platform = query.data
#     update_user_data(context.user_data["User Id"], {"Platform": platform})

#     await message.reply_text(f"Here is your link to open an account: {ACCOUNT_LINK}")
#     await message.reply_text("Please follow this manual to open your account:")
#     await context.bot.send_photo(
#         update.effective_chat.id,
#         open(GUIDE_IMAGE_PATH, "rb"),
#         "Guide to opening an account",
#     )
#     await message.reply_text("👇 How much would you like to deposit?")
#     return ASK_DEPOSIT


# async def ask_deposit(update: Update, context: CallbackContext) -> int:
#     message = update.message
#     deposit = message.text

#     if not deposit.isdigit():
#         await message.reply_text("Please type a valid amount")
#         return ASK_DEPOSIT

#     update_user_data(context.user_data["User Id"], {"Deposit": float(deposit)})

#     await message.reply_text(
#         "If you need help withdrawing, contact support. Have a great day!"
#     )
#     return ConversationHandler.END


# async def cancel(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text(
#         "👋 Goodbye! Feel free to start again anytime.",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#     return ConversationHandler.END


# def main():
#     application = Application.builder().token(TOKEN).build()
#     conv_handler = ConversationHandler(
#         [CommandHandler("start", start)],
#         {
#             SELECT_COUNTRY: [CallbackQueryHandler(select_country)],
#             ASK_COUNTRY_OTHER: [
#                 MessageHandler(filters.TEXT & ~filters.COMMAND, ask_country_other)
#             ],
#             ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
#             SELECT_PLATFORM: [CallbackQueryHandler(select_platform)],
#             ASK_DEPOSIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_deposit)],
#         },
#         [CommandHandler("start", start), CommandHandler("cancel", cancel)],
#     )

#     application.add_handler(conv_handler)

#     application.run_polling(allowed_updates=Update.ALL_TYPES)


# if __name__ == "__main__":
#     main()
