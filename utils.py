import random

def card_value(card):
    rank = card['rank']
    if rank.isdigit():
        return int(rank)
    elif rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11

def evaluate_hand(user_id):
    global players, community_cards
    player_hand = players[user_id]['hand'] + community_cards
    player_hand.sort(key=lambda x: card_value(x), reverse=True)

    # Check for different hand rankings (simplified example)
    if is_straight_flush(player_hand):
        players[user_id]['score'] = 800 + card_value(player_hand[0])
    elif is_four_of_a_kind(player_hand):
        players[user_id]['score'] = 700 + card_value(player_hand[0])
    elif is_full_house(player_hand):
        players[user_id]['score'] = 600 + card_value(player_hand[0])
    elif is_flush(player_hand):
        players[user_id]['score'] = 500 + card_value(player_hand[0])
    elif is_straight(player_hand):
        players[user_id]['score'] = 400 + card_value(player_hand[0])
    elif is_three_of_a_kind(player_hand):
        players[user_id]['score'] = 300 + card_value(player_hand[0])
    elif is_two_pair(player_hand):
        players[user_id]['score'] = 200 + card_value(player_hand[0])
    elif is_one_pair(player_hand):
        players[user_id]['score'] = 100 + card_value(player_hand[0])
    else:
        players[user_id]['score'] = card_value(player_hand[0])

# Helper functions to check for hand rankings
def is_straight_flush(hand):
    return is_straight(hand) and is_flush(hand)

def is_four_of_a_kind(hand):
    for i in range(len(hand) - 3):
        if hand[i]['rank'] == hand[i + 1]['rank'] == hand[i + 2]['rank'] == hand[i + 3]['rank']:
            return True
    return False

def is_full_house(hand):
    return is_three_of_a_kind(hand) and is_one_pair(hand)

def is_flush(hand):
    suits = set(card['suit'] for card in hand)
    return len(suits) == 1

def is_straight(hand):
    values = [card_value(card) for card in hand]
    values.sort()
    return all(values[i] == values[i - 1] + 1 for i in range(1, len(values)))

def is_three_of_a_kind(hand):
    for i in range(len(hand) - 2):
        if hand[i]['rank'] == hand[i + 1]['rank'] == hand[i + 2]['rank']:
            return True
    return False

def is_two_pair(hand):
    pairs = 0
    for i in range(len(hand) - 1):
        if hand[i]['rank'] == hand[i + 1]['rank']:
            pairs += 1
    return pairs == 2

def is_one_pair(hand):
    for i in range(len(hand) - 1):
        if hand[i]['rank'] == hand[i + 1]['rank']:
            return True
    return False


def generate_deck():
    rank = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    deck = [{'rank': rank, 'suit': suit} for rank in rank for suit in suits]
    random.shuffle(deck)
    return deck