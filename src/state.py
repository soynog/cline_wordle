"""Game state management module."""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class GameStatus(Enum):
    """Enum representing the possible game states."""
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

@dataclass
class GameState:
    """Represents the current state of the game."""
    target_word: str
    guesses: List[str]
    feedback: List[List[str]]
    used_letters: Dict[str, str]
    status: GameStatus
    remaining_attempts: int
    max_attempts: int = 6

    @classmethod
    def new_game(cls, target_word: str) -> 'GameState':
        """Create a new game state.

        Args:
            target_word: The word to guess

        Returns:
            GameState: A new game state instance
        """
        return cls(
            target_word=target_word,
            guesses=[],
            feedback=[],
            used_letters={},
            status=GameStatus.IN_PROGRESS,
            remaining_attempts=6
        )

    def update_with_guess(self, guess: str, feedback: List[str]) -> None:
        """Update the game state with a new guess.

        Args:
            guess: The guessed word
            feedback: List of feedback symbols for the guess
        """
        self.guesses.append(guess)
        self.feedback.append(feedback)
        self.remaining_attempts -= 1

        # Update used letters
        for letter, symbol in zip(guess, feedback):
            # Only update if the new status is better than the existing one
            current_status = self.used_letters.get(letter)
            if current_status is None:
                self.used_letters[letter] = symbol
            elif current_status != "✓":  # Don't downgrade from correct position
                if symbol == "✓" or (symbol == "○" and current_status == "✗"):
                    self.used_letters[letter] = symbol

        # Update game status
        if guess == self.target_word:
            self.status = GameStatus.WON
        elif self.remaining_attempts == 0:
            self.status = GameStatus.LOST

    @property
    def is_game_over(self) -> bool:
        """Check if the game is over.

        Returns:
            bool: True if the game is won or lost
        """
        return self.status in (GameStatus.WON, GameStatus.LOST)

    @property
    def current_attempt(self) -> int:
        """Get the current attempt number.

        Returns:
            int: Current attempt number (1-based)
        """
        return self.max_attempts - self.remaining_attempts + 1

    def get_statistics(self) -> Dict[str, int]:
        """Get game statistics.

        Returns:
            Dict[str, int]: Dictionary containing game statistics
        """
        return {
            "attempts": self.current_attempt,
            "remaining": self.remaining_attempts,
            "won": self.status == GameStatus.WON
        }
