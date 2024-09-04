from src.output import console_output, gui_output
from src.utils.game_utils import clear_data

def main():
    # play('console')
    play('gui')

    # Start the game
    """
    play('console')
    play('gui')
    """
    # End the game

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
