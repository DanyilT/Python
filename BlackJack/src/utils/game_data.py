import json
import os

# Determine the absolute path to the root of the project & Construct the full path to the 'to' var file
def determine_path(to, dir='data'):
    try:
        return os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')), dir, to)
    except Exception as e:
        print(f"Error during determine_path: {e}")

# Load the game data
def read_game_data(file_path=determine_path('game_data.json')):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error during read_game_data: {e}")

# Load the deck data
def read_deck(file_path=determine_path('deck.json')):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error during read_deck: {e}")

# Update player data: 'name'/'chips'/'hand' etc
def update_player_data(what_update, player_id, new_value, file_path=determine_path('game_data.json')):
    try:
        game_data = read_game_data(file_path)

        if player_id in game_data['players']:
            game_data['players'][player_id][what_update] = new_value

        with open(file_path, 'w') as file:
            json.dump(game_data, file, indent=4)
    except Exception as e:
        print(f"Error during update_player_data: {e}")

# Update the deck
def update_deck(new_deck, file_path=determine_path('deck.json')):
    try:
        with open(file_path, 'w') as file:
            json.dump({'deck': new_deck}, file, indent=4)
    except Exception as e:
        print(f"Error during update_deck: {e}")

# Update the players: add (by name) or remove (by id) a player
def update_players(what_to_do, player_id=None, player_name=None, file_path=determine_path('game_data.json')):
    try:
        game_data = read_game_data(file_path)

        if what_to_do == 'add' and player_name:
            game_data['players'][str(max(int(player_id) for player_id in game_data['players'].keys()) + 1)] = {
                "name": player_name,
                "chips": read_game_data(file_path)['settings']['chips'],
                "bet": [],
                "hand": [],
                "count_value": [],
                "status": []
            }
        elif what_to_do == 'remove' and player_id:
            # Remove the player from the players dictionary
            if player_id in game_data['players']:
                del game_data['players'][player_id]

        with open(file_path, 'w') as file:
            json.dump(game_data, file, indent=4)
    except Exception as e:
        print(f"Error during update_players: {e}")

# Update game settings: "bet", "max_players", etc.
def update_game_settings(setting, new_value, file_path=determine_path('game_data.json')):
    try:
        game_data = read_game_data(file_path)

        if 'settings' in game_data:
            game_data['settings'][setting] = new_value

        with open(file_path, 'w') as file:
            json.dump(game_data, file, indent=4)
    except Exception as e:
        print(f"Error during update_game_settings: {e}")

# I'll sell your data
