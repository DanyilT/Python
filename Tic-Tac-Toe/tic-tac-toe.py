"""
Tic-Tac-Toe Game
Using the minimax algorithm for optimal computer moves in PvC and CvC modes.

A simple console-based Tic-Tac-Toe game with multiple modes:
- Player vs Player (PvP)
- Player vs Computer (PvC)
- Computer vs Computer (CvC)
(
Created at 01/08/2025 by [DanyilT](https://github.com/DanyilT)
"""

import random
import time

from colorama import Fore, Style, init

def main():
    print(Fore.MAGENTA + "Tic-Tac-Toe!")
    init_game()


def init_game():
    """Initialize the game environment and start the game loop."""
    init(autoreset=True)    # Initialize colorama for colored output, automatically reset styles after each print

    # Ask the user to choose a game mode
    game_mode = None
    while game_mode not in ['pvp', 'pvc', 'cvc']:
        game_mode = choose_game_mode()

    # Start the game with the selected mode, initializing the board and setting the first player
    play_game(game_mode)


def choose_game_mode():
    """
    Display the game mode selection menu and prompt the user for input.

    Returns:
        str: The selected game mode as one of the following strings:
            - 'pvp' for Player vs Player
            - 'pvc' for Player vs Computer
            - 'cvc' for Computer vs Computer
        Returns None if the input is invalid.
    """
    print(Fore.CYAN + "+" + "-" * 32 + "+")
    print(Fore.CYAN + "|" + Fore.YELLOW + "        Choose Game Mode        " + Fore.CYAN + "|")
    print(Fore.CYAN + "+" + "-" * 32 + "+")
    print(Fore.CYAN + "|" + Fore.GREEN + " [1] " + Fore.WHITE + "Player vs Player (PvP)     " + Fore.CYAN + "|")
    print(Fore.CYAN + "|" + Fore.GREEN + " [2] " + Fore.WHITE + "Player vs Computer (PvC)   " + Fore.CYAN + "|")
    print(Fore.CYAN + "|" + Fore.GREEN + " [3] " + Fore.WHITE + "Computer vs Computer (CvC) " + Fore.CYAN + "|")
    print(Fore.CYAN + "+" + "-" * 32 + "+")
    choice = input(Fore.CYAN + "Enter your choice (1/2/3): " + Style.RESET_ALL).strip().lower()
    return 'pvp' if choice == '1' or choice == 'pvp' else \
           'pvc' if choice == '2' or choice == 'pvc' else \
           'cvc' if choice == '3' or choice == 'cvc' else None


def init_board():
    """Initialize the Tic-Tac-Toe board."""
    return [' '] * 9


def print_board(board):
    """
    Print the current state of the Tic-Tac-Toe board to the console.

    Args:
        board (list): A list of 9 elements representing the board cells,
                      where each element is 'X', 'O', or ' ' (empty).

    The board is displayed in a 3x3 grid with colored formatting. (dim the border)
    """
    print(Style.DIM + "+" + "-" * 13 + "+")
    for i in range(3):
        row = [board[i * 3 + j] for j in range(3)]
        print(Style.DIM + "| " + Style.RESET_ALL + " " + " | ".join(row) + " " + Style.DIM + " |")
        if i < 2: print(Style.DIM + "| " + Style.RESET_ALL + "-" * 11 + Style.DIM + " |")
    print(Style.DIM + "+" + "-" * 13 + "+")


def check_winner(board):
    """
    Check the current board for a winner or a draw.

    Args:
        board (list): A list of 9 elements representing the Tic-Tac-Toe board,
                      where each element is 'X', 'O', or ' ' (empty).

    Returns:
        str or None: Returns 'X' or 'O' if there is a winner,
                     'Draw' if the board is full and there is no winner,
                     or None if the game is still ongoing.
    """
    win_combos = [
        (0,1,2), (3,4,5), (6,7,8),  # Rows
        (0,3,6), (1,4,7), (2,5,8),  # Cols
        (0,4,8), (2,4,6)            # Diags
    ]
    for combo in win_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return board[combo[0]]
    if ' ' not in board:
        return 'Draw'
    return None


def player_move(board, player):
    """
    Prompt the player to make a move and update the board.

    Continuously asks the player for input until a valid move is entered.
    Validates that the input is a number between 1 and 9 and that the chosen cell is empty.

    Args:
        board (list): The current Tic-Tac-Toe board as a list of 9 elements.
        player (str): The current player's symbol, either 'X' or 'O'.

    Side Effects:
        Modifies the board in place by setting the chosen cell to the player's symbol.
        Prints messages to the console for invalid input or moves.
    """
    while True:
        try:
            move = int(input(f"{Fore.BLUE if player == 'X' else Fore.RED}Player {player}{Fore.GREEN}, enter your move (1-9): {Style.RESET_ALL}")) - 1
            if move < 0 or move >= 9 or board[move] != ' ':
                print(Fore.RED + "Invalid move. Try again.")
            else:
                board[move] = player
                break
        except ValueError:
            print(Fore.RED + "Please enter a valid number.")


def computer_move(board, computer='O'):
    """
    Make the optimal move for the computer using the minimax algorithm.

    Args:
        board (list): The current Tic-Tac-Toe board as a list of 9 elements.
        computer (str, optional): The computer's symbol, either 'X' or 'O'. Defaults to 'O'.

    Side Effects:
        Modifies the board in place by setting the chosen cell to the computer's symbol.
        Prints nothing.

    The function evaluates all possible moves using the minimax algorithm and selects the move
    with the highest score, ensuring the best possible outcome for the computer.
    """
    best_score = -float('inf')
    move = None
    for i in range(9):
        if board[i] == ' ':
            board[i] = computer
            score = minimax(board, False, player='X' if computer == 'O' else 'O', computer=computer)
            board[i] = ' '
            if score > best_score:
                best_score = score
                move = i
    board[move] = computer


def minimax(board, is_maximizing, player='X', computer='O'):
    """
    Recursively evaluate the board using the minimax algorithm to determine the optimal move.

    Args:
        board (list): The current Tic-Tac-Toe board as a list of 9 elements.
        is_maximizing (bool): True if it's the computer's turn to maximize the score, False for the opponent.
        player (str, optional): The opponent's symbol, either 'X' or 'O'. Defaults to 'X'.
        computer (str, optional): The computer's symbol (self), either 'X' or 'O'. Defaults to 'O'.

    Returns:
        int: The score of the board state:
            - 1 if the computer wins,
            - -1 if the player wins,
            - 0 for a draw.
    """
    winner = check_winner(board)

    # Base cases
    if winner == player:
        return -1
    elif winner == computer:
        return 1
    elif winner == 'Draw':
        return 0

    if is_maximizing:       # Own turn (computer)
        best_score = -float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = computer
                score = minimax(board, False, player=player, computer=computer)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:                   # Opponent's turn (player)
        best_score = float('inf')
        for i in range(9):
            if board[i] == ' ':
                board[i] = player
                score = minimax(board, True, player=player, computer=computer)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score


def play_game(mode, board=init_board(), current_player='X'):
    """
    Main game loop for Tic-Tac-Toe.

    Args:
        mode (str): The game mode, one of 'pvp' (Player vs Player), 'pvc' (Player vs Computer), or 'cvc' (Computer vs Computer).
        board (list, optional): The initial Tic-Tac-Toe board as a list of 9 elements. Defaults to a new empty board.
        current_player (str, optional): The symbol of the current player, either 'X' or 'O'. Defaults to 'X'. (Who is starting the game?)

    Side Effects:
        Runs the game loop, prints the board and messages to the console, and updates the board in place.

    Behavior:
        - Alternates turns between players or computer(s) based on the selected mode.
        - Handles user input, computer moves, and displays the board after each move.
        - Detects and announces the winner or a draw, then exits the loop.
    """
    while True:
        print_board(board)

        # Player vs Player (PvP)
        if mode == 'pvp':
            player_move(board, current_player)

        # Player vs Computer (PvC)
        elif mode == 'pvc':
            if current_player == 'X':
                player_move(board, 'X')  # Human
            else:
                print(Fore.YELLOW + f"AI ({current_player}) is thinking...")
                time.sleep(0.2)  # Simulate thinking time
                computer_move(board)

        # Computer vs Computer (CvC)
        elif mode == 'cvc':
            print(Fore.YELLOW + f"AI ({current_player}) is thinking...")
            time.sleep(1)  # Simulate thinking time
            if board.count(' ') == 9:
                board[random.choice([i for i in range(9)])] = current_player # Random first move
            else:
                computer_move(board, current_player)

        winner = check_winner(board)
        if winner:
            print_board(board)
            if winner == 'Draw':
                print(Fore.GREEN + Style.BRIGHT + "It's a draw! 😐")
            else:
                print((Fore.BLUE if winner == 'X' else Fore.RED) + Style.BRIGHT + ("Computer " if mode == 'pvc' and winner == 'O' or mode == 'cvc' else "Player ") + winner + Fore.GREEN + " wins! " + ("🥲" if mode == 'pvc' and winner == 'O' else "🏆"))
            break

        current_player = 'O' if current_player == 'X' else 'X'


main()
