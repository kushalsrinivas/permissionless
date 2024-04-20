from telegram import Update
from telegram.ext import ContextTypes,  Updater, CommandHandler, CallbackContext
import logging
import random
from utils import generate_deck
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
token = "6096641141:AAE7Mcdq2ybgJBxk_eA6mPwh4yNdpz4ZR-k"
username = "@PokerDokerDealer_bot"

players = {}
deck = []
community_cards = []
current_player = None
updater = Updater(token=token, use_context=True)
dp = updater.dispatcher

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global players, deck, community_cards, current_player
    players = {}
    deck = generate_deck()
    community_cards = []
    current_player = None
    return await update.message.reply_text('New poker game started. Type /join to join the game.')

def join_game(update: Update, context: CallbackContext) -> None:
    global players
    user_id = update.message.from_user.id
    if user_id not in players:
        players[user_id] = {
            'hand': [],
            'score': 0
        }
        update.message.reply_text(f'{update.message.from_user.username} joined the game.')
    else:
        update.message.reply_text('You are already in the game.')

def deal_cards(update: Update, context: CallbackContext) -> None:
    global players, deck, community_cards, current_player
    if len(players) < 2:
        update.message.reply_text('Need at least 2 players to start the game.')
        return

    # Reset player hands and community cards
    for player in players.values():
        player['hand'] = []

    community_cards = []

    # Deal two private cards to each player
    for _ in range(2):
        for player_id in players:
            card = deck.pop()
            players[player_id]['hand'].append(card)

    # Deal community cards
    for _ in range(5):
        community_cards.append(deck.pop())

    current_player = list(players.keys())[0]
    update.message.reply_text('Cards dealt. Community cards: ' + ' '.join(community_cards))
    update.message.reply_text(f"{players[current_player]['hand']} - It's {update.message.from_user.username}'s turn. Type /check or /fold.")

def check(update: Update, context: CallbackContext) -> None:
    global players, deck, community_cards, current_player
    user_id = update.message.from_user.id

    if user_id != current_player:
        update.message.reply_text("It's not your turn.")
        return

    evaluate_hand(user_id)
    update.message.reply_text(f'Your hand: {players[user_id]["hand"]} - Your score: {players[user_id]["score"]}')

    # Move to the next player or end the game
    next_player()

if __name__ == "__main__":
    print("Starting bot...")
    dp.add_handler(CommandHandler("start", start_command()))
    dp.add_handler(CommandHandler("join", join_game))
    dp.add_handler(CommandHandler("deal", deal_cards))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("fold", fold))

    # Start the Bot
    updater.start_polling()
    updater.idle()

    print("polling....")
