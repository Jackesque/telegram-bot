import datetime as dt
import re
import subprocess
from warnings import filterwarnings

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.warnings import PTBUserWarning

from utils.constants import (
    ACCOUNT_LINK,
    GUIDE_DEPOSIT_WITHDRAW_DIRECTORY_PATH,
    GUIDE_OPEN_ACCOUNT_DIRECTORY_PATH,
    PLATFORMS_KEYBOARD,
    TOKEN,
)
from utils.helpers import send_bulk_images, update_user_data

filterwarnings(
    action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
)

subprocess.run(
    ["pip", "install", "-r", "requirements.txt"],
    capture_output=True,
    text=True,
    check=False,
)

# https://blog.pythonanywhere.com/148/
print("Bot started...")
SELECT_COUNTRY, ASK_COUNTRY_OTHER, ASK_PHONE, SELECT_PLATFORM, ASK_DEPOSIT = range(5)


async def start(update: Update, context: CallbackContext) -> int:
    message = update.message
    user = update.effective_user
    timestamp = (message.date + dt.timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
    user_data = {
        "Thời gian": timestamp,
        "Id người dùng": str(user.id),
        "Username": user.username,
        "Tên": user.first_name,
        "Họ": user.last_name,
    }
    context.user_data["Id người dùng"] = str(user.id)

    update_user_data(context.user_data["Id người dùng"], user_data)

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Việt Nam", callback_data="Việt Nam"),
                InlineKeyboardButton("Hoa Kỳ", callback_data="Hoa Kỳ"),
                InlineKeyboardButton("Khác", callback_data="Khác"),
            ]
        ]
    )
    await message.reply_text("Bạn đến từ quốc gia nào?", reply_markup=reply_markup)

    return SELECT_COUNTRY


async def select_country(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    message = query.message
    selected_country = query.data
    update_user_data(context.user_data["Id người dùng"], {"Quốc gia": selected_country})

    match selected_country:
        case "Việt Nam":
            await message.reply_text("Thật tuyệt. Tôi cũng đến từ Việt Nam.")
            await message.reply_text("👇 Hãy nhập số điện thoại của bạn")

            return ASK_PHONE
        case "Hoa Kỳ":
            await message.reply_text("Xin lỗi, chúng tôi không hỗ trợ cư dân Hoa Kỳ.")
            return ConversationHandler.END
        case "Khác" | _:
            await message.reply_text("👇 Hãy nhập tên quốc gia của bạn")
            return ASK_COUNTRY_OTHER


async def ask_country_other(update: Update, context: CallbackContext) -> int:
    message = update.message
    typed_country = message.text
    update_user_data(context.user_data["Id người dùng"], {"Quốc gia": typed_country})

    await message.reply_text(
        f"{typed_country} là một đất nước tuyệt vời. Tôi đã nghe nhiều điều tốt đẹp về nó!"
    )
    await message.reply_text("👇 Số điện thoại của bạn là gì?")

    return ASK_PHONE


async def ask_phone(update: Update, context: CallbackContext) -> int:
    message = update.message
    phone = message.text

    if not re.fullmatch(r"\d{10,11}", phone):
        await message.reply_text(
            "Số điện thoại bạn nhập có vẻ không hợp lệ. Hãy nhập lại"
        )

        return ASK_PHONE

    update_user_data(context.user_data["Id người dùng"], {"SĐT": str(phone)})
    await message.reply_text(
        "Bạn đang trade trên nền tảng nào?", reply_markup=PLATFORMS_KEYBOARD
    )
    return SELECT_PLATFORM


async def select_platform(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()
    message = query.message
    platform = query.data
    update_user_data(context.user_data["Id người dùng"], {"Nền tảng": platform})

    await message.reply_text(
        f"Đây là đường link để mở tài khoản của bạn: {ACCOUNT_LINK}"
    )
    await message.reply_text("Vui lòng làm theo hướng dẫn này để mở tài khoản:")
    await send_bulk_images(
        context.bot, update.effective_chat.id, GUIDE_OPEN_ACCOUNT_DIRECTORY_PATH
    )
    await message.reply_text(
        "👇 Bạn muốn gửi bao nhiêu tiền? (VND) (hãy nhập một con số)"
    )
    return ASK_DEPOSIT


async def ask_deposit(update: Update, context: CallbackContext) -> int:
    message = update.message
    deposit = message.text

    if not deposit.isdigit():
        await message.reply_text("Hãy nhập một số tiền hợp lệ")
        return ASK_DEPOSIT

    update_user_data(
        context.user_data["Id người dùng"], {"Số tiền gửi (VND)": float(deposit)}
    )

    await message.reply_text("Vui lòng làm theo hướng dẫn này để nạp và rút tiền:")
    await send_bulk_images(
        context.bot, update.effective_chat.id, GUIDE_DEPOSIT_WITHDRAW_DIRECTORY_PATH
    )
    await message.reply_text("Chúc bạn một ngày tốt lành 🍀")
    return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "👋 Tạm biệt! Bạn có thể bắt đầu lại bất cứ lúc nào bạn muốn.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


def main():
    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        [CommandHandler("start", start)],
        {
            SELECT_COUNTRY: [CallbackQueryHandler(select_country)],
            ASK_COUNTRY_OTHER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_country_other)
            ],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            SELECT_PLATFORM: [CallbackQueryHandler(select_platform)],
            ASK_DEPOSIT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_deposit)],
        },
        [CommandHandler("start", start), CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES, timeout=60)


if __name__ == "__main__":
    main()
