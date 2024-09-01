import random
from game_data import *

# Open a new Deck of Cards
def generate_deck():
    try:
        # Define card values and their mappings
        values = {
            'A': (1, 11),
            '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            '10': 10, 'J': 10, 'Q': 10, 'K': 10
        }

        # Define suits and their symbols
        suits = {
            'Hearts': '♥',
            'Clubs': '♣',
            'Diamonds': '♦',
            'Spades': '♠'
        }

        deck = {
            f'{value}{symbol}': {
                'counts': count,    # The numeric value(s) of the card
                'value': value,     # The face value (e.g., 'A', 'K', '10')
                'suit': suit        # The suit symbol (e.g., '♥')
            }
            for suit, symbol in suits.items()
            for value, count in values.items()
        }

        update_deck(deck)
    except Exception as e:
        print(f"Error during generate_deck: {e}")

# Shuffle the Deck of Cards
def shuffle_deck(deck=read_deck()['deck']):
    try:
        deck = list(deck.items())
        random.shuffle(deck)
        update_deck(dict(deck))
    except Exception as e:
        print(f"Error during shuffle_deck: {e}")

# Throw two cards at the dealer and player(s)
def deal_hand(num_cards=2, deck=read_deck()['deck'], player_data=read_game_data()['players']):
    try:
        for player_id in player_data:
            hand = []

            for _ in range(num_cards):
                card, card_info = deck.popitem()
                hand.append({card: card_info})

            update_deck(deck)
            update_player_data('hand', player_id, hand)
            count_hand(player_id)
    except Exception as e:
        print(f"Error during deal_hand: {e}")

# Counting players hands
def count_hand(player_id, player_data=read_game_data()['players']):
    try:
        count_values = []

        for hand in player_data[player_id]['hand']:
            total = 0
            aces = 0

            for card in hand:
                card_counts = list(card.values())[0]['counts']

                if isinstance(card_counts, list):
                    total += max(card_counts)
                    aces += 1
                else:
                    total += card_counts

            while total > 21 and aces:
                total -= 10
                aces -= 1

            count_values.append(total)

        update_player_data('count_value', player_id, count_values)
    except Exception as e:
        print(f"Error during count_hand: {e}")

# Yes, just because I can
def stand(player_id):
    try:
        count_hand(player_id)
    except Exception as e:
        print(f"Error during stand: {e}")

# Hit-the-Man who is opening a card
def hit(player_id, hand_index=0, deck=read_deck()['deck'], player_data=read_game_data()['players']):
    try:
        hands = player_data[player_id]['hand']
        hand = player_data[player_id]['hand'][hand_index]

        card, card_info = deck.popitem()
        hand.append({card: card_info})

        update_deck(deck)

        hands[hand_index] = hand
        update_player_data('hand', player_id, hands)

        count_hand(player_id)
    except Exception as e:
        print(f"Error during hit: {e}")

# Double Gain/Double Risk
def double(player_id, hand_index=0, player_data=read_game_data()['players']):
    try:
        update_player_data('chips', player_id, player_data[player_id]['chips'] - player_data[player_id]['bet'])
        update_player_data('bet', player_id, player_data[player_id]['bet'] * 2)
        hit(player_id, hand_index)
    except Exception as e:
        print(f"You can't double now! Error: {e}")

# TODO: I'm not sure it work correctly (def split)
# Cut, I mean Split hand
def split(player_id, hand_index=0, deck=read_deck()['deck'], player_data=read_game_data()['players'], bet=read_game_data()['settings']['bet']):
    try:
        update_player_data('chips', player_id, player_data[player_id]['chips'] - bet)
        update_player_data('bet', player_id, player_data[player_id]['bet'] + bet)

        hands = player_data[player_id]['hand']
        hand = player_data[player_id]['hand'][hand_index]
        card1_info = list(hand[0].values())[0]
        card2_info = list(hand[1].values())[0]

        if len(hand) == 2 and card1_info['counts'] == card2_info['counts']:
            new_hand1 = [hand[0]]
            new_hand2 = [hand[1]]

            card1, card1_info = deck.popitem()
            card2, card2_info = deck.popitem()
            new_hand1.append({card1: card1_info})
            new_hand2.append({card2: card2_info})

            update_deck(deck)

            hands[hand_index] = new_hand1
            hands.insert(hand_index + 1, new_hand2)
            update_player_data('hand', player_id, hands)

            count_hand(player_id)
    except Exception as e:
        print(f"You can't split now! Error: {e}")

'''
def busted(player_id, hand_index=0):
    hands = read_game_data()['players'][player_id]['hand']
    hand = hands[hand_index]
    count_value = read_game_data()['players'][player_id]['count_value'][hand_index]

    if count_value > 21:
        print(f"Player {player_id} - Hand {hand_index + 1}: {hand} - BUST!")
        hands.pop(hand_index)
        count_hand(player_id)
'''
