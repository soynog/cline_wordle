"""Command-line interface for the Wordle game.

Handles:
- Game initialization and flow
- User input processing
- Display formatting and output
- Game state visualization
"""

from typing import Tuple
from src.controller import GameController
from src.display import DisplayManager
from src.word_manager import WordManager

# Display constants
SEPARATOR = "=" * 20
WELCOME_TEXT = """
Welcome to Command-Line Wordle!

Guess the WORDLE in 6 tries.
Each guess must be a valid 5-letter word.
After each guess, the color of the tiles will show
how close your guess was to the word.

Examples:
✓ W means the letter W is in the word and in the correct spot.
○ I means the letter I is in the word but in the wrong spot.
✗ U means the letter U is not in the word.
"""

class CLI:
    """Command-line interface for playing Wordle."""

    def __init__(self):
        """Initialize the CLI interface."""
        word_manager = WordManager()
        display_manager = DisplayManager(use_color=True)  # Explicitly enable color
        self._controller = GameController(word_manager, display_manager)
        self._display = display_manager

    def get_input(self) -> str:
        """Get and normalize user guess (empty on interrupt)."""
        try:
            return input("Enter your guess: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            return ""

    def display_welcome(self) -> None:
        """Display welcome message and game instructions."""
        print(WELCOME_TEXT)

    def display_error(self, message: str) -> None:
        """Show error using display manager's formatting."""
        self._display.show_error(message)

    def display_game_state(self) -> None:
        """Display the current game state."""
        self._display.clear_screen()
        print("\nWordle")
        print(SEPARATOR)
        print(self._display.format_game_board(
            self._controller.guesses,
            self._controller.feedback
        ))
        
        print("\nKeyboard")
        print(SEPARATOR)
        print(self._display.format_keyboard(self._controller.used_letters))
        
        # Show statistics if game is over
        if self._controller.game_over:
            stats = self._controller.statistics
            print(f"\nAttempts: {stats['attempts']}")
            print(f"Result: {'Won! 🎉' if stats['won'] else 'Lost'}")
        print()

    def display_result(self, won: bool, word: str) -> None:
        """Show game result with appropriate win/loss message."""
        message = f"\nCongratulations! The word was {word}" if won else f"\nGame Over. The word was {word}"
        self._display.show_success(message) if won else print(message)


    def play_again(self) -> bool:
        """Prompt for another game (y/n)."""
        while True:
            response = input("\nPlay again? (y/n): ").strip().lower()
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no'):
                return False
            print("Please enter 'y' or 'n'")

def main() -> None:
    """Run the game loop until player quits."""
    cli = CLI()
    cli.display_welcome()

    while True:
        cli._controller.start_game()

        while not cli._controller.game_over:
            cli.display_game_state()
            guess = cli.get_input()

            if not guess:  # Handle empty input or interrupts
                print("\nThanks for playing!")
                return

            valid, error = cli._controller.make_guess(guess)
            if not valid:
                cli._display.show_error(error)
                continue

        # Display final state
        cli.display_game_state()
        cli.display_result(cli._controller.game_won, cli._controller.target_word)

        if not cli.play_again():
            print("\nThanks for playing!")
            break

if __name__ == "__main__":
    main()
