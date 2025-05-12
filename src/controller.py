"""Game controller module for managing the Wordle game logic."""

from typing import List, Tuple
from src.state import GameState, GameStatus

class GameController:
    """Controls the main game logic and flow."""

    def __init__(self, word_manager: 'WordManager', display_manager: 'DisplayManager'):
        """Initialize the game controller with word and display managers."""
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
        """Generate feedback symbols (✓, ○, ✗) for each letter in the guess."""
        target = self._state.target_word
        feedback = ["✗"] * 5
        used_positions = set()

        # Mark correct positions first
        for i, (guess_char, target_char) in enumerate(zip(guess, target)):
            if guess_char == target_char:
                feedback[i] = "✓"
                used_positions.add(i)

        # Count remaining letters in target
        remaining = {}
        for i, char in enumerate(target):
            if i not in used_positions:
                remaining[char] = remaining.get(char, 0) + 1

        # Mark letters in wrong positions
        for i, char in enumerate(guess):
            if i not in used_positions and remaining.get(char, 0) > 0:
                feedback[i] = "○"
                remaining[char] -= 1

        return feedback

    @property
    def game_won(self) -> bool:
        """True if the player has won the game."""
        return self._state.status == GameStatus.WON

    @property
    def game_over(self) -> bool:
        """True if the game is over (won or max attempts reached)."""
        return self._state.is_game_over

    @property
    def guesses(self) -> List[str]:
        """List of guesses made so far."""
        if not self._state:
            return []
        return self._state.guesses.copy()

    @property
    def feedback(self) -> List[List[str]]:
        """Feedback for all guesses made."""
        if not self._state:
            return []
        return self._state.feedback.copy()

    @property
    def target_word(self) -> str:
        """The target word (only access when game is over)."""
        if not self._state:
            return ""
        return self._state.target_word

    @property
    def used_letters(self) -> dict:
        """Dictionary of used letters and their best status."""
        if not self._state:
            return {}
        return self._state.used_letters.copy()

    @property
    def statistics(self) -> dict:
        """Current game statistics."""
        if not self._state:
            return {"attempts": 0, "remaining": 6, "won": False}
        return self._state.get_statistics()
