import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from src.utils.game_data import determine_path, read_game_data, update_player_data, update_players, update_game_settings
from src.game_engine import generate_deck, shuffle_deck, deal_hand, hit, stand, double, split, determine_winners

# It's not main menu, it's initial menu!
class InitialMenu:
    # INITIAL!!! (pronounce as epic as possible)
    def __init__(self, root):
        self.root = root
        self.root.title("BlackJack")
        self.root.geometry('720x480')
        self.setup_ui()

    # Look it's beautiful, my initial setup
    def setup_ui(self):
        try:
            # Load icons and resize to fit square buttons
            icon_size = 32
            exit_icon = ImageTk.PhotoImage(Image.open(determine_path('exit.png', 'src/output/forGUI/icons')).resize((icon_size, icon_size)))
            settings_icon = ImageTk.PhotoImage(Image.open(determine_path('settings.png', 'src/output/forGUI/icons')).resize((icon_size, icon_size)))

            # Define configuration
            title_config = {'font': ('Fixedsys', 24), 'fg': 'black'}
            button_config = {'font': ('Fixedsys', 16), 'width': 20, 'height': 2, 'fg': 'black', 'bg': 'white', 'bd': 2}
            icon_button_config = {'width': icon_size, 'height': icon_size, 'bd': 0}

            # Create the welcome label with the defined configuration
            self.welcome_label = tk.Label(self.root, text="Welcome to the BlackJack!", **title_config)
            self.welcome_label.place(relx=0.5, rely=0.3, anchor='center')

            # Create the start button with the defined configuration
            self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game, **button_config)
            self.start_button.place(relx=0.5, rely=0.5, anchor='center')

            # Create corner buttons with the loaded icons
            self.exit_button = tk.Button(self.root, image=exit_icon, command=self.exit_game, **icon_button_config)
            self.exit_button.image = exit_icon  # Keep a reference to avoid garbage collection
            self.exit_button.place(relx=0.0, rely=0.0, x=21, y=21, anchor='nw')

            self.settings_button = tk.Button(self.root, image=settings_icon, command=self.open_settings, **icon_button_config)
            self.settings_button.image = settings_icon  # Keep a reference to avoid garbage collection
            self.settings_button.place(relx=1.0, rely=0.0, x=-21, y=21, anchor='ne')
        except Exception as e:
            print(f"Error during setup_ui: {e}")

    # Let's do this
    def start_game(self):
        try:
            self.root.withdraw()
            GUI_Play(tk.Toplevel(self.root))
        except Exception as e:
            print(f"Error during start_game: {e}")

    # No need to turn down the volume
    def open_settings(self):
        try:
            SettingsMenu(tk.Toplevel(self.root))
        except Exception as e:
            print(f"Error during open_settings: {e}")

    # I hope I'll never see you again
    def exit_game(self):
        try:
            self.root.destroy()
            self.root.quit()
        except Exception as e:
            print(f"Error during exit_game: {e}")

# Setting-petting... I mean, settings menu
class SettingsMenu:
    # Oh now the petting starts
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")
        self.root.geometry('480x360')
        self.settings = read_game_data()['settings']
        self.setup_ui()

    # Look it's beautiful, my settings setup
    def setup_ui(self):
        try:
            # Load icons and resize to fit square buttons
            icon_size = 32
            exit_icon = ImageTk.PhotoImage(Image.open(determine_path('exit.png', 'src/output/forGUI/icons')).resize((icon_size, icon_size)))
            back_icon = ImageTk.PhotoImage(Image.open(determine_path('back.png', 'src/output/forGUI/icons')).resize((icon_size, icon_size)))

            # Define configuration
            title_config = {'font': ('Fixedsys', 24), 'fg': 'black'}
            text_config = {'font': ('Fixedsys', 16), 'fg': 'black'}
            input_config = {'font': ('Fixedsys', 12), 'fg': 'black'}
            combobox_config = {'font': ('Fixedsys', 12), 'width': 15}
            button_config = {'font': ('Fixedsys', 12), 'width': 5, 'height': 1, 'fg': 'black', 'bg': 'white', 'bd': 2}
            big_red_save_button_config = {'font': ('Fixedsys', 14), 'width': 10, 'height': 1, 'fg': 'black', 'bg': 'white', 'bd': 2}
            icon_button_config = {'width': icon_size, 'height': icon_size, 'bd': 0}

            # Create the settings label with the defined configuration
            self.settings_label = tk.Label(self.root, text="Settings", **title_config)
            self.settings_label.place(relx=0.5, rely=0.2, anchor='center')

            # Create input fields for each setting
            self.entries = {}
            for idx, (setting, value) in enumerate(self.settings.items()):
                label = tk.Label(self.root, text=setting, **text_config)
                label.place(relx=0.4, rely=0.3 + idx * 0.1, anchor='e')

                if setting == 'chips' or setting == 'bet':
                    entry = ttk.Combobox(self.root, values=[str(i) for i in range(0, 1001, 10)] if setting == 'chips' else [str(i) for i in range(0, 101, 5)], font=input_config['font'])
                    entry.set(value)
                else:
                    entry = tk.Entry(self.root, font=input_config['font'])
                    entry.insert(0, value)

                entry.place(relx=0.4, rely=0.3 + idx * 0.1, anchor='w')
                self.entries[setting] = entry

            # Save button
            self.save_button = tk.Button(self.root, text="Save", command=self.save_settings, **big_red_save_button_config)
            self.save_button.place(relx=0.5, rely=0.8, anchor='center')

            # Create corner buttons with the loaded icons
            self.exit_button = tk.Button(self.root, image=exit_icon, command=self.exit_game, **icon_button_config)
            self.exit_button.image = exit_icon  # Keep a reference to avoid garbage collection
            self.exit_button.place(relx=0.0, rely=0.0, x=21, y=21, anchor='nw')

            self.back_button = tk.Button(self.root, image=back_icon, command=self.close_window, **icon_button_config)
            self.back_button.image = back_icon  # Keep a reference to avoid garbage collection
            self.back_button.place(relx=1.0, rely=0.0, x=-21, y=21, anchor='ne')

            # Add player management section
            self.add_player_label = tk.Label(self.root, text="Player Name", **text_config)
            self.add_player_label.place(relx=0.4, rely=0.5, anchor='e')

            self.add_player_entry = tk.Entry(self.root, **input_config)
            self.add_player_entry.place(relx=0.4, rely=0.5, anchor='w')

            self.add_player_button = tk.Button(self.root, text="Add", command=self.add_player, **button_config)
            self.add_player_button.place(relx=0.7, rely=0.5, anchor='w')

            self.remove_player_label = tk.Label(self.root, text="Remove Player", **text_config)
            self.remove_player_label.place(relx=0.4, rely=0.6, anchor='e')

            self.remove_player_combobox = ttk.Combobox(self.root, values=[player['name'] for player in list(read_game_data()['players'].values())[1:]], **combobox_config)
            self.remove_player_combobox.place(relx=0.4, rely=0.6, anchor='w')

            self.remove_player_button = tk.Button(self.root, text="Remove", command=self.remove_player, **button_config)
            self.remove_player_button.place(relx=0.7, rely=0.6, anchor='w')

        except Exception as e:
            print(f"Error during setup_ui: {e}")

    # Don't forget to save your work
    def save_settings(self):
        try:
            for setting, entry in self.entries.items():
                update_game_settings(setting, int(entry.get()))
            # It's incredibly fucking annoying
            # messagebox.showinfo("Save Settings", "Settings saved successfully!")
            self.close_window()
        except Exception as e:
            print(f"Error during save_settings: {e}")

    # Hello, nice man (man mean human)
    def add_player(self):
        try:
            update_players('add', player_name=self.add_player_entry.get())
            self.add_player_entry.delete(0, tk.END)
            self.remove_player_combobox['values'] = [player['name'] for player in list(read_game_data()['players'].values())[1:]]
        except Exception as e:
            print(f"Error during add_player: {e}")

    # Say goodbye, He'll not return
    def remove_player(self):
        try:
            player_name = self.remove_player_combobox.get()
            for player_id, player_info in read_game_data()['players'].items():
                if player_info['name'] == player_name:
                    update_players('remove', player_id=player_id)
                    self.remove_player_combobox['values'] = [player['name'] for player in list(read_game_data()['players'].values())[1:]]
                    break
            if player_name not in [player['name'] for player in read_game_data()['players'].values()]:
                self.remove_player_combobox.delete(0, tk.END)
        except Exception as e:
            print(f"Error during remove_player: {e}")

    # See you
    def close_window(self):
        try:
            self.root.destroy()
        except Exception as e:
            print(f"Error during close_window: {e}")

    # I hope I'll never see you again
    def exit_game(self):
        try:
            self.root.quit()
        except Exception as e:
            print(f"Error during exit_game: {e}")

# Yep, it's table. It's the easiest way to do it in tkinter
class Table:
    # Initiate table-self
    def __init__(self, root, current_turn=None):
        self.root = root
        self.current_turn = current_turn
        self.setup_ui()

    # Look it's beautiful, my table setup
    def setup_ui(self):
        try:
            # Create frame for the table
            frame = ttk.Frame(self.root)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.pack(fill='none', expand=False)

            # Create table
            columns = ['player_id', 'name', 'chips', 'bet', 'hand', 'count_value']
            columns.append('turn') if self.current_turn is not None else None
            self.tree = ttk.Treeview(frame, columns=columns, show='headings')
            self.tree.grid(sticky='nsew')

            # Set column widths
            self.tree.column('player_id', minwidth=20, width=30)
            self.tree.column('name', minwidth=100, width=150)
            self.tree.column('chips', minwidth=50, width=100)
            self.tree.column('bet', minwidth=50, width=100, anchor='center')
            self.tree.column('hand', minwidth=150, width=200, anchor='center')
            self.tree.column('count_value', minwidth=50, width=75, anchor='center')
            self.tree.column('turn', minwidth=20, width=50, anchor='e') if self.current_turn is not None else None

            # Headers
            self.tree.heading('player_id')
            self.tree.heading('name', text='Name', anchor='w')
            self.tree.heading('chips', text='Chips')
            self.tree.heading('bet', text='Bet')
            self.tree.heading('hand', text='Hand')
            self.tree.heading('count_value', text='Value')
            self.tree.heading('turn', text='Turn', anchor='e') if self.current_turn is not None else None

            # Add vertical scrollbar
            self.vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=self.vsb.set)
            self.vsb.grid(row=0, column=1, sticky='ns')

            # Add horizontal scrollbar
            self.hsb = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
            self.tree.configure(xscrollcommand=self.hsb.set)
            self.hsb.grid(row=1, column=0, sticky='ew')

            self.tree.bind('<Configure>', self.check_scrollbars)
            self.update_table()
        except Exception as e:
            print(f"Error during setup_ui: {e}")

    # Why do you have to scroll? It's not a tiktok
    def check_scrollbars(self, event):
        try:
            # Check if vertical scrollbar is needed
            if self.tree.yview() == (0.0, 1.0):
                self.vsb.grid_remove()
            else:
                self.vsb.grid()

            # Check if horizontal scrollbar is needed
            if self.tree.xview() == (0.0, 1.0):
                self.hsb.grid_remove()
            else:
                self.hsb.grid()
        except Exception as e:
            print(f"Error during check_scrollbars: {e}")

    # Sign up for our updates, it's not spam for sure
    def update_table(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            player_data = read_game_data()['players']
            for player_id, player_info in player_data.items():
                for hand_index, hand in enumerate(player_info['hand']):
                    turn_indicator = '←' if self.current_turn == [player_id, hand_index] else '' if player_id == '0' else '-' if self.current_turn is not None and (self.current_turn == ['0', 0] or int(player_id) < int(self.current_turn[0]) or (int(player_id) == int(self.current_turn[0]) and hand_index < self.current_turn[1])) else ''

                    if player_id == '0' and self.current_turn is not None and self.current_turn[0] != player_id:
                        hand_out = '? , ' + ', '.join([list(card.keys())[0] for card in hand[1:]])
                        count_value_out = '?'
                    else:
                        hand_out = ', '.join([list(card.keys())[0] for card in hand])
                        count_value_out = player_info['count_value'][hand_index]
                    bet_out = player_info['bet'][hand_index] if player_info['bet'] else ''

                    if hand_index == 0:
                        self.tree.insert('', 'end', values=(player_id, player_info['name'], player_info['chips'], bet_out, hand_out, count_value_out, turn_indicator))
                    else:
                        self.tree.insert('', 'end', values=(player_id, '', '', bet_out, hand_out, count_value_out, turn_indicator))

            if self.current_turn:
                for row in self.tree.get_children():
                    row_values = self.tree.item(row)['values']
                    if row_values[6] == '←':
                        self.tree.item(row, tags='current_turn')
                    else:
                        self.tree.item(row, tags='')

                self.tree.tag_configure('current_turn', background='#ffd966')
        except Exception as e:
            print(f"Error during update_table: {e}")

# Let's Play a Game
class GUI_Play:
    # Prepared for great purpose
    def __init__(self, root):
        self.root = root
        self.root.title("BlackJack - Desk")
        self.root.geometry("720x480")
        self.frame = ttk.Frame(self.root)
        self.setup_ui()

    def setup_ui(self):
        # Load icons and resize to fit square buttons
        icon_size = 32
        exit_icon = ImageTk.PhotoImage(Image.open(determine_path('exit.png', 'src/output/forGUI/icons')).resize((icon_size, icon_size)))
        back_icon = ImageTk.PhotoImage(Image.open(determine_path('back.png', 'src/output/forGUI/icons')).resize((icon_size, icon_size)))

        # Define configuration
        icon_button_config = {'width': icon_size, 'height': icon_size, 'bd': 0}

        # Create corner buttons with the loaded icons
        self.exit_button = tk.Button(self.root, image=exit_icon, command=self.exit_game, **icon_button_config)
        self.exit_button.image = exit_icon  # Keep a reference to avoid garbage collection
        self.exit_button.place(relx=0.0, rely=0.0, x=21, y=21, anchor='nw')

        self.back_button = tk.Button(self.root, image=back_icon, command=self.close_window, **icon_button_config)
        self.back_button.image = back_icon  # Keep a reference to avoid garbage collection
        self.back_button.place(relx=1.0, rely=0.0, x=-21, y=21, anchor='ne')

        self.run()

    # See you
    def close_window(self):
        try:
            self.root.destroy()
            InitialMenu(self.root.master).root.deiconify()
        except Exception as e:
            print(f"Error during close_window: {e}")

    # I hope I'll never see you again
    def exit_game(self):
        try:
            self.root.destroy()
            self.root.quit()
        except Exception as e:
            print(f"Error during exit_game: {e}")

    # Casino always wins
    def run(self):
        try:
            # Define configuration
            title_config = {'font': ('Fixedsys', 16), 'fg': 'black'}
            text_config = {'font': ('Fixedsys', 12), 'fg': 'black'}
            button_config = {'font': ('Fixedsys', 14), 'width': 15, 'height': 1, 'fg': 'black', 'bg': 'white', 'bd': 2}

            # Create frame for the table and buttons
            self.frame.pack(fill='both', expand=True)

            deck = {'new': False, 'shuffled': False}

            # New deck of cards
            def generate_deck_button():
                try:
                    deck['new'] = True
                    deck['shuffled'] = False
                    generate_deck()
                    update_buttons()
                except Exception as e:
                    print(f"Error during generate_deck_button: {e}")

            # Put random cards in random order
            def shuffle_deck_button():
                try:
                    deck['new'] = False
                    deck['shuffled'] = True
                    shuffle_deck()
                    update_buttons()
                except Exception as e:
                    print(f"Error during shuffle_deck_button: {e}")

            # Again? Again!
            def play_again():
                try:
                    self.frame.destroy()
                    self.frame = ttk.Frame(self.root)
                    self.setup_ui()
                except Exception as e:
                    print(f"Error during play_again: {e}")

            # Let's do this
            def start_game():
                try:
                    deal_hand()

                    self.title_label.place_forget()
                    self.tips_label.place_forget()
                    self.generate_button.place_forget()
                    self.shuffle_button.place_forget()
                    self.start_button.place_forget()

                    self.frame.place(relx=0.5, rely=0.4, anchor='center')
                    self.frame.config(relief='solid')
                    self.table = Table(self.frame, current_turn=['1', 0])

                    for player_id in list(read_game_data()['players'])[1:]:
                        # TODO: Fix this: if quit is pressed, it will continue to play (the game never ends)
                        if not self.root.winfo_exists():
                            break
                        self.player_play(player_id)

                    self.dealer_play()

                    self.table.current_turn = None
                    self.table.update_table()

                    self.winners()

                    # Show play again button
                    self.title_label.place(relx=0.5, rely=0.2, anchor='center')
                    self.tips_label.place(relx=0.5, rely=0.3, anchor='center')
                    self.generate_button.place(relx=0.5, rely=0.4, anchor='center')
                    self.shuffle_button.place_forget()
                    self.start_button.place_forget()

                    self.frame.place(relx=0.5, rely=0.41, anchor='center')
                    button_frame = ttk.Frame(self.frame)
                    button_frame.pack(pady=10)

                    self.again_button = tk.Button(button_frame, text="Play Again", command=play_again, **button_config)
                    self.again_button.pack()
                except Exception as e:
                    print(f"Error during start_game: {e}")

            # Wow they are showed and not showed
            def update_buttons():
                try:
                    if not deck['new'] and not deck['shuffled']:
                        self.title_label.config(text="Press 'Generate Deck' to open a new deck of cards")
                        self.tips_label.config(text="This will create a new deck of cards")
                        self.tips_label.place_forget()
                        self.generate_button.config(text="Generate Deck")
                        self.generate_button.place(relx=0.5, rely=0.4, anchor='center')
                        self.shuffle_button.place_forget()
                        self.start_button.place_forget()
                    elif deck['new'] and not deck['shuffled']:
                        self.title_label.config(text="Press 'Shuffle Deck' to shuffle the deck of cards")
                        self.tips_label.config(text="Deck has been opened, shuffle the deck to continue")
                        self.tips_label.place(relx=0.5, rely=0.3, anchor='center')
                        self.generate_button.place_forget()
                        self.shuffle_button.place(relx=0.5, rely=0.4, anchor='center')
                        self.start_button.place_forget()
                    elif not deck['new'] and deck['shuffled']:
                        self.title_label.config(text="Press 'Start Game' to start the game")
                        self.tips_label.config(text="Deck has been shuffled, start the game to play")
                        self.tips_label.place(relx=0.5, rely=0.3, anchor='center')
                        self.generate_button.config(text="Regenerate Deck")
                        self.start_button.place(relx=0.5, rely=0.4, anchor='center')
                        self.generate_button.place(relx=0.5, rely=0.5, anchor='center')
                        self.shuffle_button.place_forget()
                except Exception as e:
                    print(f"Error during update_buttons: {e}")

            # Create labels and buttons for generating and shuffling the deck
            self.title_label = tk.Label(self.frame, **title_config)
            self.tips_label = tk.Label(self.frame, **text_config)
            self.title_label.place(relx=0.5, rely=0.2, anchor='center')

            self.generate_button = tk.Button(self.frame, text="Generate Deck", command=generate_deck_button, **button_config)
            self.shuffle_button = tk.Button(self.frame, text="Shuffle Deck", command=shuffle_deck_button, **button_config)
            self.start_button = tk.Button(self.frame, text="Start Game", command=start_game, **button_config)

            update_buttons()

        except Exception as e:
            print(f"Error during run: {e}")

    # I lose my life
    def winners(self):
        try:
            determine_winners()
            player_data = read_game_data()['players']

            for player_id, player_info in list(player_data.items())[1:]:
                for hand_index, hand in enumerate(player_info['hand']):
                    row_tag = ''
                    if player_info['status'][hand_index] == 'win':
                        row_tag = 'win'
                    elif player_info['status'][hand_index] == 'lose':
                        row_tag = 'lose'
                    elif player_info['status'][hand_index] == 'draw':
                        row_tag = 'draw'
                    elif player_info['status'][hand_index] == 'blackjack':
                        row_tag = 'blackjack'

                    # Match the correct row by checking player_id and hand combination
                    for row in self.table.tree.get_children():
                        row_values = self.table.tree.item(row)['values']
                        if row_values[4] == ', '.join([list(card.keys())[0] for card in hand]):
                            self.table.tree.item(row, tags=row_tag)

            self.table.tree.tag_configure('win', background='#c3f3c5', foreground='white')
            self.table.tree.tag_configure('lose', background='#f5a8a8', foreground='white')
            self.table.tree.tag_configure('draw', background='#f9e79f', foreground='black')
            self.table.tree.tag_configure('blackjack', background='#d8bfd8', foreground='white')

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

                self.table.current_turn = [dealer_id, 0]
                self.table.update_table()

                if dealer_value < 17 or (dealer_value == 17 and 'A' in [card['value'] for card in dealer_hand]) or all(dealer_value < value for value in players_values):
                    hit(dealer_id)
                    self.table.update_table()
                else:
                    break

        except Exception as e:
            print(f"Error during dealer_play: {e}")

    # I'm not a player, I'm a player's play. You are bluffing
    def player_play(self, player_id):
        try:
            completed_hands = set()

            while True:
                player_info = read_game_data()['players'][player_id]
                hands = list(enumerate(player_info['hand']))

                for hand_index, hand in hands:
                    if hand_index in completed_hands:
                        continue

                    while player_info['count_value'][hand_index] < 21:
                        self.table.current_turn = [player_id, hand_index]
                        self.table.update_table()

                        action = self.action(player_id, hand_index)
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

                        player_info = read_game_data()['players'][player_id]
                        self.table.update_table()

                    completed_hands.add(hand_index)
                if hands == list(enumerate(read_game_data()['players'][player_id]['hand'])):
                    break

        except Exception as e:
            print(f"Error during player_play: {e}")

    # You can do whatever you want, but I'm not going to play with you
    def action(self, player_id, hand_index):
        try:
            action = tk.StringVar()

            def stand():
                try:
                    action.set('stand')
                    button_frame.destroy()
                except Exception as e:
                    print(f"Error during stand: {e}")

            def hit():
                try:
                    action.set('hit')
                    button_frame.destroy()
                except Exception as e:
                    print(f"Error during hit: {e}")

            def double():
                try:
                    action.set('double')
                    button_frame.destroy()
                except Exception as e:
                    print(f"Error during double: {e}")

            def split():
                try:
                    action.set('split')
                    button_frame.destroy()
                except Exception as e:
                    print(f"Error during split: {e}")

            # Define configuration
            button_config = {'font': ('Fixedsys', 12), 'width': 10, 'height': 1, 'fg': 'black', 'bg': 'white', 'bd': 2}

            # Create action buttons
            button_frame = ttk.Frame(self.frame)
            button_frame.pack(side='bottom', pady=10)

            stand_button = tk.Button(button_frame, text="Stand", command=stand, **button_config)
            stand_button.pack(side='left', padx=5)

            self.hit_button = tk.Button(button_frame, text="Hit", command=hit, **button_config)
            self.hit_button.pack(side='left', padx=5)

            if self.can_bet(player_id, hand_index):
                self.double_button = tk.Button(button_frame, text="Double", command=double, **button_config)
                self.double_button.pack(side='left', padx=5)

            if self.can_split(player_id, hand_index):
                self.split_button = tk.Button(button_frame, text="Split", command=split, **button_config)
                self.split_button.pack(side='left', padx=5)

            self.root.wait_variable(action)
            return action.get()
        except Exception as e:
            print(f"Error during action: {e}")

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
    root = tk.Tk()
    InitialMenu(root)
    root.mainloop()
