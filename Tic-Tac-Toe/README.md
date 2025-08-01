# Tic-Tac-Toe with Minimax AI

A feature-rich console-based Tic-Tac-Toe game implemented in Python with an unbeatable AI using the minimax algorithm.

[![asciicast, demo...](https://asciinema.org/a/xGGv9ypiqkq8Hzv3z1etHMuxV.svg)](https://asciinema.org/a/xGGv9ypiqkq8Hzv3z1etHMuxV)

## Features

- **Multiple Game Modes**:
  - Player vs Player (PvP)
  - Player vs Computer (PvC) - AI opponent
  - Computer vs Computer (CvC) - Watch AI play against itself

- **Smart AI**: Uses minimax algorithm for optimal moves
- **Colorful Interface**: Enhanced console display with colors
- **Input Validation**: Robust error handling for user input
- **Real-time Feedback**: Visual indicators and thinking delays

## Installation

> [!NOTE]
> You can just download the whole game as a file (it's just a one file `tic-tac-toe.py`) and don't need to clone the repository:
> 
> Notice, that this `README.md`, `LICENSE` and `requirements.txt` files will not be downloaded, so you will not have the documentation, license information and requirements file to use to download the dependencies, only the game code itself.
> 
> Source: [DanyilT/Python/Tic-Tac-Toe/](https://github.com/DanyilT/Python/blob/main/Tic-Tac-Toe/)[tic-tac-toe.py](https://github.com/DanyilT/Python/blob/main/Tic-Tac-Toe/tic-tac-toe.py)
>   ```bash
>   wget https://raw.githubusercontent.com/DanyilT/Python/refs/heads/main/Tic-Tac-Toe/tic-tac-toe.py
>   ```
1. Clone the repository:
    ```bash
    git clone https://github.com/DanyilT/Python.git
    cd Tic-Tac-Toe
    ```

2. Install dependencies:
    - Via `requirements.txt`:
      ```bash
      pip install -r requirements.txt
      ```
    - Or manually (only `colorama` is required):
      ```bash
      pip install colorama
      ```

## Usage

Run the game:
```bash
python tic-tac-toe.py
```

### Game Controls

- Choose game mode by entering `1`, `2`, or `3`
- Enter moves using numbers `1-9` corresponding to board positions:
```
 1 | 2 | 3 
-----------
 4 | 5 | 6 
-----------
 7 | 8 | 9 
```

## How It Works

### Minimax Algorithm

The AI uses the minimax algorithm to evaluate all possible game states and choose the optimal move. The algorithm:

1. **Evaluates** all possible future moves
2. **Assumes** both players play optimally
3. **Maximizes** the AI's score while minimizing the opponent's
4. **Guarantees** the best possible outcome for the AI

### Game Modes

- **PvP**: Two human players take turns
- **PvC**: Human vs _unbeatable AI_ (you play as X, AI as O)
- **CvC**: Watch two AI players compete (first move is random for variety)

## Code Structure

- `main()`: Entry point and game initialization
- `init_game`: It should be the main function, but I use `main()` just to call this (`init_game`) function... That's it...
- `choose_game_mode()`: Mode selection interface
- `init_board()`: Initializes the empty game board (array of 9 `' '` elements)
- `print_board()`: Colored board display
- `check_winner()`: Win/draw detection
- `player_move()`: Human input handling
- `computer_move()`: AI move execution
- `minimax()`: AI decision-making algorithm (minimax)
- `play_game()`: Main game loop handling all modes

## Algorithm Performance

The minimax algorithm evaluates all possible game states, making the AI unbeatable when playing optimally. In Computer vs Computer mode, the game will always end in a draw when both players play perfectly.

## Dependencies

- `colorama`: For colored console output
- `random`: For randomizing first moves in CvC mode
- `time`: For simulating AI thinking delays

## License

This project is open source and available under the [MIT License](/LICENSE) - see LICENSE file for details.
