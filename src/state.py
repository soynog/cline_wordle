"""Game state management module.

Handles game state tracking including:
- Game status (in progress/won/lost)
- Guess history and feedback
- Letter usage tracking
- Attempt counting
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class GameStatus(Enum):
    """Game status values.
    
    IN_PROGRESS: Game is active and accepting guesses
    WON: Player correctly guessed the word
    LOST: Player used all attempts without winning
    """
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"

@dataclass
class GameState:
    """Game state container tracking all game-related data."""
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
        """Update state with new guess and its feedback.
        
        Records the guess and feedback, updates letter statuses,
        and checks for win/loss conditions.
        """
        # Record guess and update attempts
        self.guesses.append(guess)
        self.feedback.append(feedback)
        self.remaining_attempts -= 1

        # Update letter statuses (✓ > ○ > ✗)
        for letter, new_status in zip(guess, feedback):
            current = self.used_letters.get(letter)
            
            # Always record new letters
            if current is None:
                self.used_letters[letter] = new_status
                continue
                
            # Never downgrade from ✓
            if current == "✓":
                continue
                
            # Upgrade to ✓ or from ✗ to ○
            if new_status == "✓" or (new_status == "○" and current == "✗"):
                self.used_letters[letter] = new_status

        # Check win/loss conditions
        if guess == self.target_word:
            self.status = GameStatus.WON
        elif self.remaining_attempts == 0:
            self.status = GameStatus.LOST

    @property
    def is_game_over(self) -> bool:
        """True if the game is won or lost."""
        return self.status in (GameStatus.WON, GameStatus.LOST)

    @property
    def current_attempt(self) -> int:
        """Current attempt number (0-based)."""
        return self.max_attempts - self.remaining_attempts

    def get_statistics(self) -> Dict[str, int]:
        """Game statistics including attempts, remaining tries, and win status."""
        return {
            "attempts": self.current_attempt,
            "remaining": self.remaining_attempts,
            "won": self.status == GameStatus.WON
        }
