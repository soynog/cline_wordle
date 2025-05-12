"""Command-line interface for the Wordle game."""

from typing import Optional, List, Dict
from src.controller import GameController
from src.display import DisplayManager
from src.word_manager import WordManager

class CLI:
    """Handles command-line interface interactions."""

    def __init__(self):
        """Initialize the CLI interface."""
        word_manager = WordManager()
        display_manager = DisplayManager(use_color=True)  # Explicitly enable color
        self._controller = GameController(word_manager, display_manager)
        self._display = display_manager

    def get_input(self) -> str:
        """Get user input for word guess.

        Returns:
            str: The user's guess in uppercase.
        """
        try:
            return input("Enter your guess: ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            return ""

    def display_welcome(self) -> None:
        """Display the welcome message and game instructions."""
        print("\nWelcome to Command-Line Wordle!")
        print("\nGuess the WORDLE in 6 tries.")
        print("Each guess must be a valid 5-letter word.")
        print("After each guess, the color of the tiles will show")
        print("how close your guess was to the word.\n")
        print("Examples:")
        print("✓ W means the letter W is in the word and in the correct spot.")
        print("○ I means the letter I is in the word but in the wrong spot.")
        print("✗ U means the letter U is not in the word.\n")

    def display_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: The error message to display.
        """
        print(f"Error: {message}")

    def display_game_state(self) -> None:
        """Display the current game state."""
        self._display.clear_screen()
        print("\nWordle")
        print("=" * 20)
        print(self._display.format_game_board(
            self._controller.guesses,
            self._controller.feedback
        ))
        
        print("\nKeyboard")
        print("=" * 20)
        print(self._display.format_keyboard(self._controller.used_letters))
        
        # Show statistics if game is over
        if self._controller.game_over:
            stats = self._controller.statistics
            print(f"\nAttempts: {stats['attempts']}")
            print(f"Result: {'Won! 🎉' if stats['won'] else 'Lost'}")
        print()

    def display_result(self, won: bool, word: str) -> None:
        """Display the game result.

        Args:
            won: Whether the player won the game.
            word: The target word.
        """
        if won:
            print(f"\nCongratulations! The word was {word}")
        else:
            print(f"\nGame Over. The word was {word}")


    def play_again(self) -> bool:
        """Ask if the player wants to play again.

        Returns:
            bool: True if the player wants to play again
        """
        while True:
            response = input("\nPlay again? (y/n): ").strip().lower()
            if response in ('y', 'yes'):
                return True
            if response in ('n', 'no'):
                return False
            print("Please enter 'y' or 'n'")

def main() -> None:
    """Main entry point for the game."""
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
