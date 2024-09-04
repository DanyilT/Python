from src.utils.game_data import *

# How much do you mind to lose?
def bet_and_chips(chips=read_game_data()['settings']['chips'], bet=read_game_data()['settings']['bet']): # It's not ok to use read_game_data() here, but it's just for the sake of simplicity. If you want to use this function, you should pass the chips and bet values as arguments. When the program starts, it will use the default values from the settings.json file and aplied to chips and bet variables and if somthing will changed in the settings.json file, it will not be reflected in the chips and bet variables if you don't restart the program or set the values manually.
    try:
        update_game_settings('chips', chips)    # Default 100 chips
        update_game_settings('bet', bet)        # Default 10 bet
    except Exception as e:
        print(f"Error during bet_and_chips: {e}")

# Oh shit, I'm naked
def show_data(data='all'):
    try:
        deck = read_deck()['deck']
        player_data = read_game_data()['players']
        settings = read_game_data()['settings']

        if data in ['deck', 'all']:
            print("Deck Information:")
            print(f"Total cards in deck: {len(deck)}")
            for card_key, card_details in deck.items():
                print(f"{card_key}: {card_details}")
            print("\n")
        if data in ['players', 'all']:
            print("Players Information:")
            for player_id, player_info in player_data.items():
                print(f"Player ID: {player_id}")
                for key, value in player_info.items():
                    print(f"{key}: {value}")
            print("\n")
        if data in ['settings', 'all']:
            print("Game Settings:")
            for setting, value in settings.items():
                print(f"{setting}: {value}")
            print("\n")
    except Exception as e:
        print(f"Error during show_data: {e}")

# Oops, I'll take it
def clear_data(clear='all'):
    try:
        player_data = read_game_data()['players']

        if clear in ['chips', 'all']:
            for player_id in list(player_data)[1:]:
                update_player_data('chips', player_id, 0)
                update_player_data('bet', player_id, [])
                update_player_data('status', player_id, [])
        if clear in ['hand', 'all']:
            for player_id in player_data:
                update_player_data('hand', player_id, [])
                update_player_data('count_value', player_id, [])
        if clear in ['deck', 'all']:
            update_deck({})
    except Exception as e:
        print(f"Error during clear_data: {e}")

# It's not a cheating, I swear
def probability(probability='all', hide_first_dealer_card=True):
    try:
        deck = read_deck()['deck']

        # Add the dealer's first card to the deck if it should be hidden. This is to ensure that the probability of drawing
        if hide_first_dealer_card:
            dealer_first_card = list(read_game_data()['players']['0']['hand'][0][0].keys())[0]
            deck[dealer_first_card] = read_game_data()['players']['0']['hand'][0][0][dealer_first_card]

        # Count occurrences of each card value and suit in the deck
        card_counts = {}
        suit_counts = {}
        for card, card_info in deck.items():
            card_counts[card_info['value']] = 1 if card_info['value'] not in card_counts else card_counts[card_info['value']] + 1
            suit_counts[card_info['suit']] = 1 if card_info['suit'] not in suit_counts else suit_counts[card_info['suit']] + 1

        probabilities = {}

        # Calculate the probability of drawing each card value
        probabilities['card'] = {value: (count / len(deck)) * 100 for value, count in card_counts.items()}

        # Calculate the combined probability for cards with value 10 (10, J, Q, K)
        probabilities['one-ten'] = {**{key: value for key, value in probabilities['card'].items() if key not in ['10', 'J', 'Q', 'K']}, '10/J/Q/K': sum(probabilities['card'].get(value, 0) for value in ['10', 'J', 'Q', 'K'])}

        # Calculate the combined probability for low cards (2-6) and high cards (7-A)
        probabilities['low/high'] = {'2-6': sum(probabilities['card'].get(value, 0) for value in ['2', '3', '4', '5', '6']), '7-A': sum(probabilities['card'].get(value, 0) for value in ['7', '8', '9', 'A'])}

        # Calculate the probability for each suit
        probabilities['suit'] = {suit: (count / len(deck)) * 100 for suit, count in suit_counts.items()}

        # Print probabilities based on the specified parameter
        if probability in ['card', 'all']:
            print("Card Probabilities:")
            for value, rate in sorted(probabilities['card'].items(), key=lambda item: item[1], reverse=True):
                print(f"{value} - {rate:.2f}%")
        if probability in ['one-ten', 'all']:
            print("\nOne ten Value Probabilities:")
            for value, rate in sorted(probabilities['one-ten'].items(), key=lambda item: item[1], reverse=True):
                print(f"{value} - {rate:.2f}%")
        if probability in ['low/high', 'all']:
            print("\nLow/High Value Probabilities:")
            for value, rate in sorted(probabilities['low/high'].items(), key=lambda item: item[1], reverse=True):
                print(f"{value} - {rate:.2f}%")
        if probability in ['suit', 'all']:
            print("\nSuit Probabilities:")
            for suit, rate in sorted(probabilities['suit'].items(), key=lambda item: item[1], reverse=True):
                print(f"{suit} - {rate:.2f}%")

    except Exception as e:
        print(f"Error during probability: {e}")
