# Blackjack Game

This project is implementation of a Blackjack game using Python and Tkinter for the graphical user interface (GUI). The game allows multiple players to play against a dealer.

## Features

- The game is implemented in Python.
- The game has a graphical user interface (GUI) built using Tkinter.
- Multiple players can join the game.
- It's a table.
- The game follows the standard Blackjack rules.

### How to Play / Rules

**Objective**: The goal of the game is to have a hand value that is closer to 21 than the dealer's hand value without exceeding 21.

1. Dealer open new deck of cards and shuffle them.
2. Dealer deals two cards to each player and one open card and one closed card to themselves.
3. Each player starts with a certain number of chips.
4. Players place their bets.
5. Players take turns to `hit`, `stand`, `double`, or `split` based on their hand.
   - `Hit`: Take another card from the deck.
   - `Stand`: Keep the current hand value and end the turn.
   - `Double`: Double the bet and take one more card. After that, the player must stand.
   - `Split`: If the player has two cards of the same rank, they can split them into two separate hands. The player must place an additional bet equal to the original bet.
6. The dealer plays according to the game rules.
7. The game determines the winner based on the hand values.
8. Players win or lose chips based on the outcome of the game.
   - **Blackjack**: If a player's hand value is exactly 21 with the first two cards, they have a Blackjack and win 1.5 times the bet amount.
   - **Win**: If the player's hand value is closer to 21 than the dealer's hand value without exceeding 21 or the dealer busts, the player wins the bet.
   - **Lose**: If the player's hand value exceeds 21 or is lower than the dealer's hand value, the player loses the bet.
   - **Draw**: If the player's hand value is equal to the dealer's hand value, the bet is returned to the player.

## Requirements

- Python 3.x
- For graphical user interface (GUI):
  - Tkinter (usually included with Python installations)
  - Pillow (Python Imaging Library)

### Installation

Just Google it, if you don't know how to install Python, Tkinter or Pillow. Ask ChatGpt for any help.

#### Windows

1. Download and install the latest version of Python from the [official Python website](https://www.python.org/downloads/). Ensure that you check the box to add Python to your PATH during installation.
2. Install Pillow (download if you want to use qui version of the game):
    ```sh
    pip install pillow
    ```

#### macOS

1. Install Homebrew (trust me you need it, you can't install Python without it):
    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2. Install Python using Homebrew:
     ```sh
     brew install python
     ```
3. Install Pillow (download if you want to use qui version of the game):
    ```sh
    pip3 install pillow
    ```

#### Linux

- If you are using a Linux, I think you already know what to do. You don't need my help.

## Usage

### Clone the Repository

1. Clone the repository:
    ```sh
    git clone https://github.com/DanyilT/Python.git
    ```

2. Navigate to the project folder:
   - For Windows:
        ```sh
        cd Python\BlackJack
        ```
   - For macOS and Linux:
        ```sh
        cd Python/BlackJack
        ```

3. Run the main script to start the game:
   - For Windows:
        ```sh
        python main.py
        ```
   - For macOS and Linux:
        ```sh
        python3 main.py
        ```

4. The program will ask `Enter 'console' for console output or 'gui' for GUI output:`
   - Enter `console` to play the game in the console.
   - Enter `gui` to play the game with the graphical user interface (GUI).

## File Structure

The project is organized into several directories and files, each serving a specific purpose. Below is a detailed description of the file structure:

- `data/`: Contains JSON data files used in the game.
  - `deck.json`: Contains the deck of cards used in the game.
  - `game_data.json`: Contains the player information and settings.
- `src/`: Contains the source code for the game.
  - `output/`: Contains the output modules for the game.
    - `forGUI/icons/..`: Contains the icons used in the GUI.
    - `console_output.py`: Contains the logic for running the game in the console. It handles player actions, game flow, and displaying game information in the console.
    - `gui_output.py`: Contains the logic for running the game with a graphical user interface (GUI) using Tkinter. It manages the GUI elements and player interactions through the GUI.
  - `utils/`: Contains utility modules used in the game.
    - `game_data.py`: Contains functions to load and update game data from the JSON files.
    - `game_utils.py`: Contains utility functions used throughout the game, such as clearing game data or show probability of the next card and more useful functions.
- `game.py`: Entry point of the application. This script initializes the game and handles user input to choose between console and GUI output.
- `README.md`: You are reading it right now.
