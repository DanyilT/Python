from src.output import console_output, gui_output
from src.utils.game_utils import clear_data

# Yep, this is the whole code, only one line of code
def main():
    # Start the game
    play(input("Enter 'console' for console output or 'gui' for GUI output: "))
    # End the game

    """
    play('console')
    play('gui')
    """

    # Clear the data (optional)
    clear_data()

# Yes this is the start, not the main function
def play(output='console'):
    if output == 'console':
        console_output.main()
    elif output == 'gui':
        gui_output.main()

if __name__ == "__main__":
    main()
