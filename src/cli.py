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
        display_manager = DisplayManager()
        self._controller = GameController(word_manager, display_manager)
        self._display = display_manager
        self._used_letters: Dict[str, str] = {}

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

    def display_game_state(self, guesses: List[str], feedback: List[List[str]]) -> None:
        """Display the current game state.

        Args:
            guesses: List of previous guesses.
            feedback: List of feedback for each guess.
        """
        self._display.clear_screen()
        print("\nWordle")
        print("=" * 20)
        print(self._display.format_game_board(guesses, feedback))
        print("\nKeyboard")
        print("=" * 20)
        print(self._display.format_keyboard(self._used_letters))
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

    def update_used_letters(self, guess: str, feedback: List[str]) -> None:
        """Update the keyboard state with used letters.

        Args:
            guess: The guessed word
            feedback: Feedback for the guess
        """
        for letter, status in zip(guess, feedback):
            # Only update if the new status is better than the existing one
            current_status = self._used_letters.get(letter)
            if current_status is None or (current_status != "✓" and (status == "✓" or current_status == "✗")):
                self._used_letters[letter] = status

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
        cli._used_letters.clear()

        while not cli._controller.game_over:
            cli.display_game_state(cli._controller.guesses, cli._controller.feedback)
            guess = cli.get_input()

            if not guess:  # Handle empty input or interrupts
                print("\nThanks for playing!")
                return

            valid, error = cli._controller.make_guess(guess)
            if not valid:
                cli._display.show_error(error)
                continue

            # Update keyboard state with the latest guess
            latest_guess = cli._controller.guesses[-1]
            latest_feedback = cli._controller.feedback[-1]
            cli.update_used_letters(latest_guess, latest_feedback)

        # Display final state
        cli.display_game_state(cli._controller.guesses, cli._controller.feedback)
        cli.display_result(cli._controller.game_won, cli._controller.target_word)

        if not cli.play_again():
            print("\nThanks for playing!")
            break

if __name__ == "__main__":
    main()
