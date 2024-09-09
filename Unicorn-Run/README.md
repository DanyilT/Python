# Unicorn Run

Unicorn Run is a 2D side-scrolling game built using Python and Pygame. The player controls a unicorn, avoiding enemies and collecting bonuses to score points.

## Features

- Main Menu: Start a new game, continue a paused game, or exit.
- Pause Functionality: Pause the game and return to the main menu.
- Game Over Screen: Display the player's score, top scores, and options to restart or exit to the main menu.
- Responsive UI: Adjusts to window resizing.

### How to Play

#### Controls

- **Enter**: Start a new game or continue a paused game.
- **Letter keys**: Enter your name on Main Menu.
- **Arrow Keys / WASD**: Move the unicorn.
- **ESC**: Pause the game / Exit the game if on the main menu.
- **Mouse**: Interact with buttons in the main menu and game over screen.

#### Gameplay

1. **Start the Game**: Launch the game and press the play button in the main menu.
2. **Control the Unicorn**: Use the arrow keys to move the unicorn.
3. **Avoid Enemies**: Dodge enemies to stay alive.
4. **Collect Bonuses**: Gather bonuses to increase your score.
5. **Pause/Resume**: Press `ESC` to pause and return to the main menu.
6. **Game Over**: When the game ends, view your score and top scores, and choose to restart or exit.

## Requirements

- Python 3.x
- Pygame

### Installation

Just Google it, if you don't know how to install Python or PyGame. Ask ChatGpt for any help.

### Windows

1. Download and install the latest version of Python from the [official Python website](https://www.python.org/downloads/). Ensure that you check the box to add Python to your PATH during installation.
2. Install PyGame using pip:
    ```sh
    pip install pygame
    ```

### macOS

1. Install Homebrew (trust me you need it, you can't install Python without it):
    ```sh
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2. Install Python using Homebrew:
     ```sh
     brew install python
     ```
3. Install PyGame using pip:
    ```sh
    pip3 install pygame
    ```

### Linux

- If you are using a Linux, I think you already know what to do. You don't need my help.

## Usage

### Clone the Repository

#### Using Git

1. Clone the repository:
    ```sh
    git clone https://github.com/DanyilT/Python.git
    ```

2. Navigate to the project folder:
   - For Windows:
        ```sh
        cd Python\Unicorn-Run
        ```
   - For macOS and Linux:
        ```sh
        cd Python/Unicorn-Run
        ```

#### Downloading the ZIP File

1. Download the ZIP file from the [GitHub repository](https://github.com/DanyilT/Python.git) and extract it.
2. Navigate to the project folder in the extracted directory (`Python/Unicorn-Run`).

### Run the Script

- For Windows:
    ```sh
    python game.py
    ```
- For macOS and Linux:
    ```sh
    python3 game.py
    ```

## File Structure

- `images/..`: Contains game assets (background, player, enemies, bonuses, icons).
- `data.json`: Stores player scores.
- `game.py`: Game script.
- `README.md`: You are reading it right now.

### Classes and Functions in `game.py`

- `Main_Menu`: Displays the main menu and handles user input.
    - `__init__`: Initializes the main menu.
    - `show(self)`: Displays the main menu.
    - `ui(self)`: Draws the main menu UI.
    - `display_input_field(self)`: Displays the input field for the player's name.
    - `display_top_scores(self)`: Displays the top scores.
- `Game`: Initializes the game and manages game states.
    - `__init__`: Initializes the game.
    - `run(self)`: Runs the game loop.
    - `ui(self)`: Draws the game UI.
    - `update_player(self, player_rect)`: Updates the player's position.
    - `create_player(self)`: Creates the player sprite.
    - `create_enemy(self)`: Creates an enemy sprite.
    - `create_bonus(self)`: Creates a bonus sprite.
    - `save_score(self)`: Saves the player's score to the data file.
    - `pause(self)`: Pauses the game and show pause modal.
    - `game_over(self)`: Displays the game over screen.
- `Game_Data`: Manages player data and scores.
    - `__init__`: Initializes the game data.
    - `load_player_data(self)`: Loads player scores from the data file.
    - `save_player_data(self)`: Saves player scores to the data file.
    - `get_relative_path(self, filename, directory)`: Returns the relative path of a file.
- `if __name__ == '__main__'`: Initializes the game
