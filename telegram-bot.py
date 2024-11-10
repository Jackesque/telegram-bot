from telegram.ext import Application, CommandHandler, MessageHandler, filters
from constants import TOKEN

print("Starting the bot...")

async def start_command(update, context):
    await update.message.reply_text('Hi! Welcome to our bot.')

async def help_command(update, context):
    await update.message.reply_text('Helping...\nDone!')

async def echo(update, context):
    await update.message.reply_text(update.message.text)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()
