import json

# Load the game data
def read_game_data(file_path='data/game_data.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load the deck data
def read_deck(file_path='data/deck.json'):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save the game data
def write_game_data(data, file_path='data/game_data.json'):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Update player data: "name"/"chips"/"hand"
def update_player_data(what_update, player_id, new_value, file_path='data/game_data.json'):
    game_data = read_game_data(file_path)
    
    if player_id in game_data['players']:
        game_data['players'][player_id][what_update] = new_value
    
    write_game_data(game_data, file_path)

# Update the deck
def update_deck(new_deck, file_path='data/deck.json'):
    with open(file_path, 'w') as file:
        json.dump({"deck": new_deck}, file, indent=4)

# Update game settings: "bet", "max_players", etc.
def update_game_settings(setting, new_value, file_path='data/game_data.json'):
    game_data = read_game_data(file_path)
    
    if 'settings' in game_data:
        game_data['settings'][setting] = new_value
    
    write_game_data(game_data, file_path)

# I'll sell your data