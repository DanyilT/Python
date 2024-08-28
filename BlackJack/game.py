import random
from game_data import *
from console_output import draw_table, action

# Function to start the game
def main():
    set_bet_for_all_players() # Need my attecntionsanjcv,..d
    generate_deck()
    shuffle_deck()
    deal_hand()

    # For colsole
    game_loop('console')



    # draw_table()

    # # split_hand("1")
    # # clear_data()
    # print(len(read_deck()['deck']))
зн
    # for player_id, player_info in read_game_data()['players'].items():
    #     if player_id != '0':
    #         update_player_data('bet', player_id, read_game_data()['settings']['bet'])
    #         chips = read_game_data()['settings']['chips'] - read_game_data()['settings']['bet'] # I think i have remove this
    #         update_player_data('chips', player_id, chips)


def player_play(player_id):
    # Get player data
    player_info = read_game_data()['players'][player_id]
    hands_to_play = list(enumerate(player_info['hand']))  # List of (hand_index, hand) tuples

    while hands_to_play:
        # Get the index and hand for the current play
        hand_index, current_hand = hands_to_play.pop(0)

        # Ask for the player's action
        can_split_hand = can_split(player_id, current_hand)
        action_choice = action(player_info['name'], can_split=can_split_hand, hand=hand_index)

        if action_choice == "stand":
            # Player stands, move on to the next hand or player
            continue
        
        elif action_choice == "hit":
            # Player chooses to hit, draw a card for the current hand
            hit(player_id, hand_index)
        
        elif action_choice == "double":
            # Player chooses to double, check for enough chips, then draw a card and double the bet
            if player_info['chips'] >= player_info['bet']:
                double(player_id, hand_index)
                # After doubling, the player automatically stands
                continue
            else:
                print("Not enough chips to double. Please choose another action.")
        
        elif action_choice == "split":
            # Player chooses to split, check if the split is possible
            if can_split(player_id, current_hand):
                split(player_id, hand_index)
                # After splitting, we need to add both new hands to the list of hands to play
                # Each new hand must be processed in the same loop
                player_info = read_game_data()['players'][player_id]  # Refresh player data
                hands_to_play.extend(list(enumerate(player_info['hand'][hand_index:])))

            else:
                print("Cannot split this hand. Please choose another action.")
        
        # Re-fetch player data and hand info after any action
        player_info = read_game_data()['players'][player_id]
        hands_to_play = list(enumerate(player_info['hand']))  # Update hands_to_play in case of split



# You are bluffing
def player_play(player_id, hand, action):
    if action == "stand":
        continue
    elif action == "hit":
        hit(player_id, hand)
    elif action == "double" and read_game_data()['players'][player_id]['chips'] - read_game_data()['players'][player_id]['bet'] >= 0:
        double(deck, hand)
    elif action == "split" and can_split(hand) and read_game_data()['players'][player_id]['chips'] - read_game_data()['players'][player_id]['bet'] >= 0:
        split(player_id)
    else:
        continue

def action(player_name, can_split=False, hand=None):
    for last_chance_to_make_a_decision in range(3):
        action = input(f"{player_name}{' - Hand ' + str(hand) if hand else ''}, what would you like to do? (hit/stand/double{('/split' if can_split else '')}): ").lower()
        action = 'hit' if action in ['hit', 'h', '1'] else 'stan' if action in ['stand', 's', '2', ''] else 'double' if action in ['double', 'd', '3'] else 'split' if action in ['split', '4'] else None

        if action in ['hit', 'stand', 'double', 'split']:
            return action
        else:
            print("Invalid action, please choose 'hit', 'stand', 'double', or 'split'.")
    return = 'stand'

# def dealer_play():
#     dealer_info = read_game_data()['players']['0']
#     dealer_hand_value = max([value for value in dealer_info['count_value'] if value <= 21], default=0)
    
#     # Calculate the best value for each player
#     player_best_values = []
#     for player_id, player_info in read_game_data()['players'].items():
#         if player_id == '0':  # Skip the dealer
#             continue
#         player_best_value = max([value for value in player_info['count_value'] if value <= 21], default=0)
#         player_best_values.append(player_best_value)
    
#     while dealer_hand_value < 17 or any(dealer_hand_value < player_value for player_value in player_best_values):
#         # The dealer hits (draws a card)
#         new_card = hit('0')
#         dealer_info['hand'].append(new_card)

#         # Recalculate the hand's values
#         dealer_info['count_value'] = calculate_hand_value(dealer_info['hand'])
#         dealer_hand_value = max([value for value in dealer_info['count_value'] if value <= 21], default=0)
        
#         print(f"Dealer hits and draws: {new_card}")
#         print(f"Dealer's current hand: {dealer_info['hand']} with value: {dealer_hand_value}")

#         # Check if the dealer's hand has busted (gone over 21)
#         if dealer_hand_value > 21:
#             print("Dealer busts!")
#             break

#     # Update the dealer's hand and count_value in the game data
#     update_player_data('hand', '0', dealer_info['hand'])
#     update_player_data('count_value', '0', dealer_info['count_value'])

#     return dealer_hand_value




# # Win jeckpot, wait realy?
# def determine_winners():
#     winners = []
#     dealer_value = max([value for value in dealer_info['count_value'] if value <= 21], default=0)

#     for player_id, player_info in read_game_data()['players'].items():
#         if player_id == '0':
#             continue

#         player_results = ['win': 0, 'draw': 0, 'lose': 0]

#         for value in player_info['count_value']:
#             if value > dealer_best_value and value <= 21:
#                 player_results['win'] += 1 
#             elif value == dealer_best_value and value <= 21:
#                 player_results['draw']
#             else:
#                 player_results['lose'] += 1

#         player_gain = player_info['chips']
#         player_gain += 2 * player_info['bet'] * player_results['win']
#         player_gain -= player_info['bet'] * player_results['lose']
#         player_gain += player_info['bet'] * player_results['draw']

#         update_player_data('chips', player_id, player_gain)
#         update_player_data('bet', player_id, 0)


#         if player_results['win'] > 0:
#             winners.append(player_info['name'])
#     return winners

# Money first
def set_bet_for_all_players():
    for player_id, player_info in read_game_data()['players'].items():
        if player_id != '0':
            update_player_data('bet', player_id, read_game_data()['settings']['bet'])
            chips = read_game_data()['settings']['chips'] - read_game_data()['settings']['bet'] # I think i have remove this
            update_player_data('chips', player_id, chips)

# Open a new Deck of Cards
def generate_deck():
    deck = {}
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

# Shuffle the Deck of Cards
def shuffle_deck():
    deck = list(read_deck()['deck'].items())
    random.shuffle(deck)
    update_deck(dict(deck))

# Throw two cards at the dealer and player(s)
def deal_hand(num_cards=2):
    deck = read_deck()['deck']

    for player_id in read_game_data()['players']:
        hand = []
        for _ in range(num_cards):
            card, card_info = deck.popitem()
            hand.append({card: card_info})
        update_player_data('hand', player_id, hand)
        update_player_data('count_value', player_id, count_hand(player_id))
    update_deck(deck)

# Counting players hands
def count_hand(player_id):
    hands = read_game_data()['players'][player_id]['hand']
    count_values = []

    if isinstance(hands[0], list):
        for hand in hands:
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

        for card in hands:
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

    return count_values

# Is it really possible to split?
def can_split(player_id, hand):
    return len(hand) == 2 and list(hand[0].values())[0]['counts'] == list(hand[1].values())[0]['counts'] and read_game_data()['players'][player_id]['chips'] >= read_game_data()['players'][player_id]['bet']

# TODO: chexk it
# Cut, I mean Split hand
def split(player_id, hand_index=0):
    deck = read_deck()['deck']
    player = read_game_data()['players'][player_id]
    hand = player['hand'][hand_index]
    
    if len(hand) == 2:
        card1_info = list(hand[0].values())[0]
        card2_info = list(hand[1].values())[0]
        
        if card1_info['counts'] == card2_info['counts']:
            # Create two new hands
            new_hand1 = [hand[0]]
            new_hand2 = [hand[1]]
            
            # Deal one new card to each new hand
            card1, card1_info = deck.popitem()
            card2, card2_info = deck.popitem()
            new_hand1.append({card1: card1_info})
            new_hand2.append({card2: card2_info})

            # Replace the original hand with the first new hand and insert the second hand
            player['hand'][hand_index] = new_hand1
            player['hand'].insert(hand_index + 1, new_hand2)

            # Update count values for all hands
            count_values = [count_specific_hand(hand) for hand in player['hand']]
            update_player_data('count_value', player_id, count_values)
            
            # Adjust bet and chips
            new_bet = player['bet'] + read_game_data()['settings']['bet']
            new_chips = player['chips'] - read_game_data()['settings']['bet']
            update_player_data('bet', player_id, new_bet)
            update_player_data('chips', player_id, new_chips)
            
            update_deck(deck)

# Hit-the-Man who is opening a card
def hit(player_id, hand_index=0):
    deck = read_deck()['deck']
    hand = read_game_data()['players'][player_id]['hand'][hand_index]

    card, card_info = deck.popitem()
    hand.append({card: card_info})
    
    player_hands = read_game_data()['players'][player_id]['hand']
    player_hands[hand_index] = hand
    update_player_data('hand', player_id, player_hands)

    player_counts = [count_specific_hand(h) for h in player_hands]
    update_player_data('count_value', player_id, player_counts)

    update_deck(deck)

# Double Gain/Double Risk
def double(player_id, hand_index=0):
    hit(player_id, hand_index)
    update_player_data('chips', player_id, read_game_data()['players'][player_id]['chips'] - read_game_data()['players'][player_id]['bet'])
    update_player_data('bet', player_id, read_game_data()['players'][player_id]['bet'] * 2)

# Oops, I'll take it
def clear_data(clear='hand'):
    if clear == 'hand':
        for player_id in read_game_data()['players']:
            update_player_data('hand', player_id, [])
            update_player_data('count_value', player_id, [])
    elif clear == 'deck':
        update_deck({})

if __name__ == "__main__":
    main()
