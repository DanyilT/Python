import random
import re
import time
from src.utils.game_utils import probability
from src.utils.game_data import read_game_data, update_player_data
from src.game_engine import generate_deck, shuffle_deck, deal_hand, stand, hit, double, split, determine_winners

# Look it's my table! I'm so proud of it. Isn't it beautiful? Look it's so colorful! It has no legs, but it's still a table
class Table:
    # Initiate table-self. Prepared for great purpose
    def __init__(self, current_turn=None):
        self.current_turn = current_turn
        self.rows = []

    # Wow I'm an artist, am I?
    def draw(self):
        try:
            player_data = read_game_data()['players']
            for player_id, player_info in player_data.items():
                name = self.colorize(player_info['name'], 'White') if player_id == '0' and self.current_turn is not None and self.current_turn[0] == player_id else self.colorize(player_info['name'], 'Black') if player_id == '0' else self.colorize(player_info['name'])

                for hand_index, hand in enumerate(player_info['hand']):
                    turn_indicator = '←' if self.current_turn == [player_id, hand_index] else 'D' if player_id == '0' else '-' if self.current_turn is not None and (self.current_turn == ['0', 0] or int(player_id) < int(self.current_turn[0]) or (int(player_id) == int(self.current_turn[0]) and hand_index < self.current_turn[1])) else ''

                    if player_id == '0' and self.current_turn is not None and self.current_turn[0] != player_id:
                        hand_out = '? , ' + ', '.join(self.colorize(card_key, card_info['suit']) for card in hand[1:] for card_key, card_info in card.items())
                        count_value_out = '?'
                    else:
                        hand_out = ', '.join(self.colorize(card_key, card_info['suit']) for card in hand for card_key, card_info in card.items())
                        count_value_out = player_info['count_value'][hand_index]

                    bet_out = player_info['bet'][hand_index] if player_info['bet'] is not None else ''

                    # Row in rows with rows. more rows
                    if hand_index == 0:
                        row = [
                            player_id,
                            name,
                            str(player_info['chips']),
                            str(bet_out),
                            hand_out,
                            count_value_out,
                            turn_indicator
                        ]
                    else:
                        row = [
                            player_id,
                            '',
                            '',
                            str(bet_out),
                            hand_out,
                            count_value_out,
                            turn_indicator
                        ]

                    self.rows.append(row)
            self.print_out()
        except Exception as e:
            print(f"Error during draw: {e}")

    # Coming out! I'm... oh not there
    def print_out(self):
        try:
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

            headers = ['', 'Name', 'Chips', 'Bet', 'Hand', 'Value', 'Turn']

            header_line = (
                f"{headers[0].ljust(table_width['num_width'])} | "
                f"{headers[1].ljust(table_width['name_width'])} | "
                f"{headers[2].ljust(table_width['chips_width'])} | "
                f"{headers[3].ljust(table_width['bet_width'])} | "
                f"{headers[4].ljust(table_width['cards_width'])} | "
                f"{headers[5].ljust(table_width['counts_width'])}"
            )

            if self.current_turn is not None:
                header_line += f" | {headers[6].ljust(table_width['turn_width'])}"

            print(header_line)
            print("-" * (sum(table_width.values()) + len(table_width) * 3 - 3))

            for row in self.rows:
                row_line = (
                    f"{str(row[0]).ljust(table_width['num_width'])} | "
                    f"{str(row[1]).ljust(table_width['name_width'] + len(str(row[1])) - len(self.strip_color(str(row[1]))))} | "
                    f"{str(row[2]).ljust(table_width['chips_width'])} | "
                    f"{str(row[3]).ljust(table_width['bet_width'])} | "
                    f"{str(row[4]).ljust(table_width['cards_width'] + len(str(row[4])) - len(self.strip_color(str(row[4]))))} | "
                    f"{str(row[5]).ljust(table_width['counts_width'])}"
                )

                if self.current_turn is not None:
                    row_line += f" | {row[6].ljust(table_width['turn_width'])}"

                print(row_line)
        except Exception as e:
            print(f"Error during print_out: {e}")

    # It's Rainbow uwu
    def colorize(self, text, color=None):
        try:
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
        except Exception as e:
            print(f"Error during colorize: {e}")
            return text

    # Exterminate color, Only noir allowed
    def strip_color(self, text):
        try:
            return re.sub(r'\033\[\d+m', '', text)
        except Exception as e:
            print(f"Error during strip_color: {e}")
            return text

# Do you want play with me? This class will generate/shuffle/deal cards and it will play the game and determine the winners, it's ask for action from the player and do the action based on the player's input and the game state (can_bet, can_split, etc.) and dealer's action and determine the winners
class Console_Play:
    # Prepared for great purpose
    def __init__(self):
        self.players = read_game_data()['players'] # It's better to remove this line and use read_game_data()['players'] directly in the methods
        generate_deck()
        shuffle_deck()
        deal_hand()

    # Casino always wins
    def run(self):
        try:
            player_data = read_game_data()['players']
            # print("Table:")
            # Table().draw()
            print("Players' turn:")
            for player_id in list(player_data)[1:]:
                time.sleep(1)

                self.player_play(player_id)
                print()

            time.sleep(1)

            print("Dealer's turn:")
            self.dealer_play()

            time.sleep(1)

            print("\nWinners:")
            self.winners()

            main() if input("Would you like to play again? (Y/n): ").lower() in ['y', 'yes', ''] else None

        except Exception as e:
            print(f"Error during run: {e}")

    # I lose my life
    def winners(self):
        try:
            determine_winners()
            player_data = read_game_data()['players']

            for player_id, player_info in list(player_data.items())[1:]:
                print(f"Player {player_info['name']}:")

                for hand_index, result in enumerate(player_info['status']):
                    print(f" Hand {hand_index + 1} {Table().colorize(result, 'Green' if result == 'win' else 'Red' if result == 'lose' else 'Yellow' if result == 'draw' else 'Magenta' if result == 'blackjack' else None)} with cards: {[list(card.keys())[0] for card in player_info['hand'][hand_index]]}")

                print(f" Chips: {player_info['chips']}\n")

        except Exception as e:
            print(f"Error during winners: {e}")

    # Unforeseeable Dealer's actions
    def dealer_play(self, dealer_id='0'):
        try:
            player_data = read_game_data()['players']
            players_values = [value for player_id, player_info in player_data.items() if player_id != dealer_id for value in player_info['count_value'] if value <= 21]

            while True:
                player_data = read_game_data()['players']  # Refresh player data
                dealer_hand = player_data[dealer_id]['hand'][0]
                dealer_value = player_data[dealer_id]['count_value'][0]

                Table(current_turn=[dealer_id, 0]).draw()

                if dealer_value < 17 or (dealer_value == 17 and 'A' in [card['value'] for card in dealer_hand]) or all(dealer_value < value for value in players_values):
                    print("Dealer hits")
                    hit(dealer_id)
                else:
                    print("Dealer busts") if dealer_value > 21 else print("Dealer stands")
                    break

                time.sleep(2)

        except Exception as e:
            print(f"Error during dealer_play: {e}")

    # I'm not a player, I'm a player's play. You are bluffing
    def player_play(self, player_id, show_probability=False):
        try:
            completed_hands = set()

            while True:
                player_info = read_game_data()['players'][player_id]
                hands = list(enumerate(player_info['hand']))

                for hand_index, hand in hands:
                    if hand_index in completed_hands:
                        continue

                    while player_info['count_value'][hand_index] < 21:
                        Table(current_turn=[player_id, hand_index]).draw()

                        # Should I hit or should I stand?
                        probability('low/high') if show_probability else None

                        action = self.action(player_info['name'], self.can_bet(player_id, hand_index), self.can_split(player_id, hand_index), hand)

                        if action == 'stand':
                            stand(player_id)
                            completed_hands.add(hand_index)
                            break
                        elif action == 'hit':
                            hit(player_id, hand_index)
                        elif action == 'double' and self.can_bet(player_id, hand_index):
                            double(player_id, hand_index)
                            completed_hands.add(hand_index)
                            break
                        elif action == 'split' and self.can_split(player_id, hand_index):
                            split(player_id, hand_index)
                        elif action == 'easter':
                            update_player_data('chips', player_id, 999999999)
                            update_player_data('bet', player_id, [0])
                            update_player_data('count_value', player_id, [21])
                            break

                        # Refresh player data
                        player_info = read_game_data()['players'][player_id]
                        hand = player_info['hand'][hand_index]
                    completed_hands.add(hand_index)

                    print(f"Player {player_info['name']} busts with hand {str([list(card.keys())[0] for card in hand])}") if player_info['count_value'][hand_index] > 21 else print(f"Player {player_info['name']} have 21 with hand {str([list(card.keys())[0] for card in hand])}") if player_info['count_value'][hand_index] == 21 else print(f"Player {player_info['name']} stands with hand {str([list(card.keys())[0] for card in hand])}")

                if hands == list(enumerate(read_game_data()['players'][player_id]['hand'])):
                    break

        except Exception as e:
            print(f"Error during player_play: {e}")

    # You can do whatever you want, but I'm not going to play with you
    def action(self, player_name, can_bet=False, can_split=False, hand=None):
        try:
            for last_chance_to_make_a_decision in range(3):
                action = input(f"{player_name}{' - Hand ' + str([list(card.keys())[0] for card in hand])}, what would you like to do? (hit/stand{'/double' if can_bet else ''}{('/split' if can_split else '')}): ").lower()
                action = 'stand' if action in ['stand', 's', '2', ''] else 'hit' if action in ['hit', 'h', '1'] else 'double' if action in ['double', 'd', '3'] else 'split' if action in ['split', '4'] else 'egg' if action == 'qwerty' else None

                if action in ['stand', 'hit', 'double', 'split']:
                    return action
                elif action == 'egg':
                    return 'easter'
                else:
                    # Don't forget to comment next line
                    # print("Fuck you!\n You really can't spell right? Take your fucking keyboard and write STAND or HIT or DOUBLE or SPLIT!! Is it really so hard? I have to write two whole lines of code to tell you that you don't know how to write!")
                    print(f"Invalid action, please choose hit, stand{', double' if can_bet else ''}{', split' if can_split else ''}")
            return 'stand'
        except Exception as e:
            print(f"Error during action: {e}")
            return 'stand'

    # I'm poor ukrainian student, can you be my sugar daddy?
    def can_bet(self, player_id, hand_index=0):
        try:
            return read_game_data()['players'][player_id]['chips'] >= read_game_data()['players'][player_id]['bet'][hand_index]
        except Exception as e:
            print(f"Error during can_bet: {e}")
            return False

    # Is it really possible to split?
    def can_split(self, player_id, hand_index=0):
        try:
            return len(read_game_data()['players'][player_id]['hand'][hand_index]) == 2 and list(read_game_data()['players'][player_id]['hand'][hand_index][0].values())[0]['counts'] == list(read_game_data()['players'][player_id]['hand'][hand_index][1].values())[0]['counts'] and self.can_bet(player_id, hand_index)
        except Exception as e:
            print(f"Error during can_split: {e}")
            return False

def main():
    Console_Play().run()
