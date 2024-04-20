from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

token = "7084157416:AAFuOQ2rZCbEpagFH8U0oyygZv7ORLOVgpg"
username = "@diehard_degen_bot"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await update.message.reply_text("hello this is a wowuwo")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await update.message.reply_text("this is a help message")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await update.message.reply_text("this is a help message")


def handle_responses(text: str) -> str:
    text = text.lower()
    if 'hello' in text:
        return "Hey there"
    elif 'how are you' in text:
        return "hola amiga , kaise ho theeko ?"
    else:
        return "check"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'user ({update.message.chat.id}) in ({message_type}) : "{text}" ')

    if message_type == "group":
        if username in text:
            new_text: str = text.replace(username, " ").strip()
            response: str = handle_responses(new_text)
        else:
            return
    else:
        response: str = handle_responses(text)
    print(response)
    await update.message.reply_text(response)


async def Error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update  ({update}) caused the following error : {context.error}")


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(token).build()
    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(Error)

    print("polling....")
    app.run_polling(poll_interval=5)