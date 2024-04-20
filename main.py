from telegram import Update
from telegram.ext import ContextTypes,  Updater, CommandHandler, CallbackContext
import logging
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = "6096641141:AAE7Mcdq2ybgJBxk_eA6mPwh4yNdpz4ZR-k"
username = "@PokerDokerDealer_bot"

players = {}
deck = []
community_cards = []
current_player = None

def generate_deck():
    rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [{'rank': rank, 'suit': suit} for rank in rank for suit in suits]
    random.shuffle(deck)
    return deck
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, deck, community_cards, current_player
    players = {}
    deck = generate_deck()
    community_cards = []
    current_player = None
    return await update.message.reply_text('New poker game started. Type /join to join the game.')

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
