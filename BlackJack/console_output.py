import random
import re
from game_data import read_game_data

# Wow I'm an artist, am I? You really don't want to know how does it work
def draw_table(current_turn=None):
    # Prepared for great purpose
    rows = []

    # Row in rows with rows. more rows
    for player_id, player_info in read_game_data()['players'].items():
        name = colorize(player_info['name'], 'Black') if player_id == '0' else colorize(player_info['name'])
        turn_indicator = '←' if int(player_id) == current_turn else 'D' if int(player_id) == 0 else '-' if current_turn is not None and int(player_id) < current_turn or current_turn == 0 else ''

        if player_id == '0':
            if current_turn == player_id:
                hand = ', '.join(colorize(card_key, card_info['suit']) for card in player_info['hand'] for card_key, card_info in card.items())
                count_value = ', '.join(map(str, player_info['count_value']))
            else:
                hand = '? , ' + ', '.join(colorize(card_key, card_info['suit']) for card in player_info['hand'][1:] for card_key, card_info in card.items())
                count_value = '?'

            row = [
                player_id,
                name,
                str(player_info['chips']),
                str(player_info['bet']),
                hand,
                count_value
            ]
        else:
            if player_info['hand'] and isinstance(player_info['hand'][0], list):
                for i, hand_of_hands in enumerate(player_info['hand']):
                    hand = ', '.join(colorize(card_key, card_info['suit']) for card in hand_of_hands for card_key, card_info in card.items())
                    count_value = ', '.join(map(str, player_info['count_value'][i]))

                    if i == 0:
                        row = [
                            player_id,
                            name,
                            str(player_info['chips']),
                            str(player_info['bet']),
                            hand,
                            count_value
                        ]
                    else:
                        row = [
                            "",  # Empty ID
                            "",  # Empty Name
                            "",  # Empty Chips
                            "",  # Empty Bet
                            hand,
                            count_value
                        ]
                        turn_indicator = ''
            else:
                hand = ', '.join(colorize(card_key, card_info['suit']) for card in player_info['hand'] for card_key, card_info in card.items())
                count_value = ', '.join(map(str, player_info['count_value']))

                row = [
                    player_id,
                    name,
                    str(player_info['chips']),
                    str(player_info['bet']),
                    hand,
                    count_value
                ]
                
        row.append(turn_indicator)
        rows.append(row)

    def print_out():
        # I'm not fat
        table_width = {
            'num_width': 3,
            'name_width': 15,
            'chips_width': 10,
            'bet_width': 5,
            'cards_width': 25,
            'counts_width': 5,
            'turn_width': 5
        }

        # Print Header
        headers = ["", "Name", "Chips", "Bet", "Hand", "Value", "Turn"]

        header_line = (
            f"{headers[0].ljust(table_width['num_width'])} | "
            f"{headers[1].ljust(table_width['name_width'])} | "
            f"{headers[2].ljust(table_width['chips_width'])} | "
            f"{headers[3].ljust(table_width['bet_width'])} | "
            f"{headers[4].ljust(table_width['cards_width'])} | "
            f"{headers[5].ljust(table_width['counts_width'])}"
        )

        if current_turn is not None:
            header_line += f" | {headers[6].ljust(table_width['turn_width'])}"
        
        print(header_line)
        print("-" * (sum(table_width.values()) + len(table_width) * 3 - 3))

        # Print Table rows
        for row in rows:
            row_line = (
                f"{str(row[0]).ljust(table_width['num_width'])} | "
                f"{str(row[1]).ljust(table_width['name_width'] + len(row[1]) - len(strip_color(row[1])))} | "
                f"{str(row[2]).ljust(table_width['chips_width'])} | "
                f"{str(row[3]).ljust(table_width['bet_width'])} | "
                f"{str(row[4]).ljust(table_width['cards_width'] + len(row[4]) - len(strip_color(row[4])))} | "
                f"{str(row[5]).ljust(table_width['counts_width'])}"
            )
            
            if current_turn is not None:
                row_line += f" | {row[6].ljust(table_width['turn_width'])}"
            
            print(row_line)

    print_out()

# You can do whatever you want
def action(player_name, can_split=False, hand=None):
    for last_chance_to_make_a_decision in range(3):
        action = input(f"{player_name}{' - Hand ' + str(hand) if hand else ''}, what would you like to do? (hit/stand/double{('/split' if can_split else '')}): ").lower()
        action = 'hit' if action in ['hit', 'h', '1'] else 'stan' if action in ['stand', 's', '2', ''] else 'double' if action in ['double', 'd', '3'] else 'split' if action in ['split', '4'] else None

        if action in ['hit', 'stand', 'double', 'split']:
            return action
        else:
            print("Invalid action, please choose 'hit', 'stand', 'double', or 'split'.")
    return = 'stand'

# It's Rainbow uwu
def colorize(text, color=None):
    color_codes = {
        'Black': '\033[90m',
        'Red': '\033[91m',
        'Green': '\033[92m',
        'Yellow': '\033[93m',
        'Blue': '\033[94m',
        'Magenta': '\033[95m',
        'Cyan': '\033[96m',
        'White': '\033[97m',
        'Reset': '\033[0m'
    }
    
    suit_to_color = {
        'Clubs': 'Black',
        'Spades': 'Black',
        'Hearts': 'Red',
        'Diamonds': 'Red'
    }

    if color in suit_to_color:
        color = suit_to_color[color]

    if color in color_codes:
        return f"{color_codes[color]}{text}{color_codes['Reset']}"
    else:
        return f"{color_codes[random.choice(list(color_codes.keys())[1:-2])]}{text}{color_codes['Reset']}"

# Exterminate color, Only noir allowed
def strip_color(text):
    return re.sub(r'\033\[\d+m', '', text)

# It's my firt or second, I stopped counting, try to achive this:
'''
# Good luck to understand what's happening here. If you figure it out, please tell me
def console_output(deck, dealer_hand, players, player_hands, current_turn):
    # Regex and Fun to remove ANSI color codes
    def strip_color(text):
        ansi_escape = re.compile(r'\x1b\
                                        [([0-9]+)(;[0-9]+)*m')
        return ansi_escape.sub('', text)

    # Wow I'm an artist, am I? You really don't want to know how does it works
    def draw_table():
        card_colors = {
            'Hearts': '\033[91m',   # Red
            'Clubs': '\033[90m',    # Black
            'Diamonds': '\033[91m', # Red
            'Spades': '\033[90m',   # Black
            'Reset': '\033[0m'      # Reset
        }

        table_width = {
            'num_width': 3,
            'name_width': 15,
            'cards_width': 25,
            'turn_width': 5
        }

        headers = ["Num", "Player Name", "Cards", "Turn"]

        # Print header
        print(f"{headers[0]:<{table_width['num_width']}} | {headers[1]:<{table_width['name_width']}} | {headers[2]:<{table_width['cards_width']}} | {headers[3]:<{table_width['turn_width']}}")
        print("-" * (table_width['num_width'] + table_width['name_width'] + table_width['cards_width'] + table_width['turn_width'] + 10))

        # Print dealer's row
        if current_turn is None or current_turn == 0:
            dealer_cards = ", ".join(f"{card_colors[card_info['suit']]}{card_key}{card_colors['Reset']}" for card_key, card_info in dealer_hand[0].items())
        else:
            dealer_cards = "? , " + ", ".join(f"{card_colors[card_info['suit']]}{card_key}{card_colors['Reset']}" for card_key, card_info in dealer_hand[1].items())

        print(f"{'0':<{table_width['num_width']}} | {'\033[34mDealer\033[0m':<{table_width['name_width'] + len('\033[34mDealer\033[0m') - len(strip_color('\033[34mDealer\033[0m'))}} | {dealer_cards:<{table_width['cards_width'] + len(dealer_cards) - len(strip_color(dealer_cards))}} | {"←" if current_turn is None or current_turn == 0 else "D":<{table_width['turn_width']}}")

        # Print each player's row
        for player_num, player_info in players.items():
            player_name = player_info[0]
            hands = player_hands[player_name]

            if isinstance(hands[0], list):  # Player has split hands
                for i, hand in enumerate(hands):
                    cards = ", ".join(f"{card_colors[card_info['suit']]}{card_key}{card_colors['Reset']}" for card in hand for card_key, card_info in card.items())
                    print(f"{player_num + i:<{table_width['num_width']}} | {player_name} - Hand {i+1:<{table_width['name_width'] - len(player_name) - 10}} | {cards:<{table_width['cards_width'] + len(cards) - len(strip_color(cards))}} | {'-' if player_num < current_turn or current_turn is None or current_turn == 0 else '←' if player_num == current_turn else '':<{table_width['turn_width']}}")
            else:
                cards = ", ".join(f"{card_colors[card_info['suit']]}{card_key}{card_colors['Reset']}" for card_key, card_info in hands.items())
                print(f"{player_num:<{table_width['num_width']}} | {player_name:<{table_width['name_width']}} | {cards:<{table_width['cards_width'] + len(cards) - len(strip_color(cards))}} | {'-' if player_num < current_turn or current_turn is None or current_turn == 0 else '←' if player_num == current_turn else '':<{table_width['turn_width']}}")


    print(f"Total cards in deck: {len(deck)}")
    print("\n")

    draw_table()
'''
