from telegram import Update
from telegram.ext import ContextTypes,   Updater, CommandHandler, CallbackContext
import logging
import random
from utils import generate_deck , evaluate_hand

token = "6096641141:AAE7Mcdq2ybgJBxk_eA6mPwh4yNdpz4ZR-k"
username = "@PokerDokerDealer_bot"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher

# Poker Game State
players = {}
deck = []
community_cards = []
current_player = None

# Function to start a new poker game
def start_game(update: Update, context: CallbackContext) -> None:
    global players, deck, community_cards, current_player
    players = {}
    deck = generate_deck()
    community_cards = []
    current_player = None
    update.message.reply_text('New poker game started. Type /join to join the game.')

# Function to join the poker game
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

# Function to deal cards to players and community
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

# Function to check the current player's hand
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

# Function to fold and skip to the next player
def fold(update: Update, context: CallbackContext) -> None:
    global players, deck, community_cards, current_player
    user_id = update.message.from_user.id

    if user_id != current_player:
        update.message.reply_text("It's not your turn.")
        return

    update.message.reply_text(f'{update.message.from_user.username} folded.')
    next_player()

# Function to move to the next player or end the game
def next_player():
    global players, deck, community_cards, current_player
    player_ids = list(players.keys())
    current_player_index = player_ids.index(current_player)

    if current_player_index < len(players) - 1:
        current_player = player_ids[current_player_index + 1]
        updater.bot.send_message(current_player, f"It's your turn. Type /check or /fold.")
    else:
        end_game()

# Function to end the game and determine the winner
def end_game(update: Update, context: CallbackContext ):
    global players, deck, community_cards, current_player
    winner_id = max(players, key=lambda x: players[x]['score'])
    update.message.reply_text(f'{update.message.from_user.username} wins with a score of {players[winner_id]["score"]}!')
    update.message.reply_text('Game over. Type /start to play again.')


if __name__ == "__main__":
    print("Starting bot...")
    dp.add_handler(CommandHandler("start", start_game))
    dp.add_handler(CommandHandler("join", join_game))
    dp.add_handler(CommandHandler("deal", deal_cards))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("fold", fold))

    # Start the Bot
    updater.start_polling()
    updater.idle()

    print("polling....")
