from game_engine import generate_deck, shuffle_deck, deal_hand
from console_output import Console_Play

def main():
    # Start the game
    play()
    # End the game

# Yes this is the start, not the main function
def play(output='console'):
    generate_deck()
    shuffle_deck()
    deal_hand()
    if output == 'console':
        Console_Play().run()


if __name__ == "__main__":
    main()
