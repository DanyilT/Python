import random
from src.utils.game_data import *

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
def shuffle_deck():
    try:
        deck = list(read_deck()['deck'].items())
        random.shuffle(deck)
        update_deck(dict(deck))
    except Exception as e:
        print(f"Error during shuffle_deck: {e}")

# Throw two cards at the dealer and player(s)
def deal_hand(num_cards=2, dealer_id='0'):
    try:
        deck = read_deck()['deck']
        player_data = read_game_data()['players']
        chips = read_game_data()['settings']['chips']
        bet = read_game_data()['settings']['bet']

        for player_id in player_data:
            if player_id != dealer_id:
                update_player_data('bet', player_id, [bet])
                update_player_data('chips', player_id, chips - bet)

            hand = []

            for _ in range(num_cards):
                card, card_info = deck.popitem()
                hand.append({card: card_info})

            update_deck(deck)
            update_player_data('hand', player_id, [hand])
            count_hand(player_id)
    except Exception as e:
        print(f"Error during deal_hand: {e}")

# Counting players hands
def count_hand(player_id):
    try:
        player_data = read_game_data()['players']
        count_values = []

        if isinstance(player_data[player_id]['hand'][0], list):
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
        else:
            total = 0
            aces = 0

            for card in player_data[player_id]['hand']:
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
def hit(player_id, hand_index=0):
    try:
        deck = read_deck()['deck']
        player_data = read_game_data()['players']

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
def double(player_id, hand_index=0):
    try:
        player_data = read_game_data()['players']
        bets = player_data[player_id]['bet']

        update_player_data('chips', player_id, player_data[player_id]['chips'] - bets[hand_index])
        bets[hand_index] *= 2
        update_player_data('bet', player_id, bets)
        hit(player_id, hand_index)
    except Exception as e:
        print(f"You can't double now! Error: {e}")

# Cut, I mean Split hand
def split(player_id, hand_index=0):
    try:
        deck = read_deck()['deck']
        player_data = read_game_data()['players']
        bets = player_data[player_id]['bet']
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

            bets.insert(hand_index + 1, bets[hand_index])
            update_player_data('chips', player_id, player_data[player_id]['chips'] - bets[hand_index])
            update_player_data('bet', player_id, bets)

            count_hand(player_id)
    except Exception as e:
        print(f"You can't split now! Error: {e}")

# Hit the jackpot? Wait really?
def determine_winners():
    try:
        player_data = read_game_data()['players']
        dealer_value = max([value for value in player_data['0']['count_value'] if value <= 21], default=0)

        for player_id, player_info in list(player_data.items())[1:]:
            bets = player_info['bet']
            status = [''] * len(player_info['hand'])

            for hand_index, hand in enumerate(player_info['hand']):
                if len(hand) == 2 and player_info['count_value'][hand_index] == 21:
                    status[hand_index] = 'blackjack'
                    bets[hand_index] = player_info['bet'][hand_index] * 2.5
                else:
                    if player_info['count_value'][hand_index] > dealer_value and player_info['count_value'][hand_index] <= 21:
                        status[hand_index] = 'win'
                        bets[hand_index] = player_info['bet'][hand_index] * 2
                    elif player_info['count_value'][hand_index] == dealer_value:
                        status[hand_index] = 'draw'
                    else:
                        status[hand_index] = 'lose'
                        bets[hand_index] = 0

            update_player_data('status', player_id, status)
            update_player_data('chips', player_id, player_data[player_id]['chips'] + sum(bets))
    except Exception as e:
        print(f"Error during determine_winners: {e}")
