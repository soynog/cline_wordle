"""Game controller module for managing the Wordle game logic."""

from typing import List, Tuple
from src.state import GameState, GameStatus

class GameController:
    """Controls the main game logic and flow."""

    def __init__(self, word_manager, display_manager):
        """Initialize the game controller.

        Args:
            word_manager: Component for managing words and validation
            display_manager: Component for managing game display
        """
        self._word_manager = word_manager
        self._display_manager = display_manager
        self._state = None

    def start_game(self) -> None:
        """Start a new game with a new target word."""
        target_word = self._word_manager.get_random_word()
        self._state = GameState.new_game(target_word)

    def make_guess(self, guess: str) -> Tuple[bool, str]:
        """Process a player's guess.

        Args:
            guess: The player's guessed word

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
            - is_valid: True if the guess was valid and processed
            - error_message: Error message if the guess was invalid
        """
        if self._state.is_game_over:
            return False, "Game is already over"

        if len(guess) != 5:
            return False, "Guess must be 5 letters"

        if not self._word_manager.is_valid_word(guess):
            return False, "Not a valid word"

        feedback = self._generate_feedback(guess)
        self._state.update_with_guess(guess, feedback)
        return True, ""

    def _generate_feedback(self, guess: str) -> List[str]:
        """Generate feedback for a guess.

        Args:
            guess: The player's guessed word

        Returns:
            List[str]: List of feedback symbols for each letter
            - "✓" for correct letter in correct position
            - "○" for correct letter in wrong position
            - "✗" for letter not in word
        """
        feedback = ["✗"] * 5
        target_chars = list(self._state.target_word)
        guess_chars = list(guess)

        # First pass: mark correct positions
        for i in range(5):
            if guess_chars[i] == target_chars[i]:
                feedback[i] = "✓"
                target_chars[i] = None
                guess_chars[i] = None

        # Second pass: mark correct letters in wrong positions
        remaining_target = [c for c in target_chars if c is not None]
        for i in range(5):
            if guess_chars[i] is None:
                continue
            if guess_chars[i] in remaining_target:
                feedback[i] = "○"
                remaining_target.remove(guess_chars[i])

        return feedback

    @property
    def game_won(self) -> bool:
        """Check if the game has been won.

        Returns:
            bool: True if the game has been won
        """
        return self._state.status == GameStatus.WON

    @property
    def game_over(self) -> bool:
        """Check if the game is over.

        Returns:
            bool: True if the game is over (won or max attempts reached)
        """
        return self._state.is_game_over

    @property
    def guesses(self) -> List[str]:
        """Get the list of guesses made.

        Returns:
            List[str]: List of guesses made so far
        """
        return self._state.guesses.copy()

    @property
    def feedback(self) -> List[List[str]]:
        """Get the feedback for all guesses.

        Returns:
            List[List[str]]: List of feedback for each guess
        """
        return self._state.feedback.copy()

    @property
    def target_word(self) -> str:
        """Get the target word (for when game is over).

        Returns:
            str: The target word
        """
        return self._state.target_word

    @property
    def used_letters(self) -> dict:
        """Get the dictionary of used letters and their status.

        Returns:
            dict: Dictionary mapping letters to their status
        """
        return self._state.used_letters.copy()

    @property
    def statistics(self) -> dict:
        """Get the current game statistics.

        Returns:
            dict: Dictionary containing game statistics
        """
        return self._state.get_statistics()
