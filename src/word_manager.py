"""Word management module for handling word selection and validation.

Uses a dual dictionary system:
- Solution words: Common 5-letter words that can be answers
- Valid guesses: All acceptable 5-letter words for guessing

Solution words are automatically included in valid guesses.
All words are converted to uppercase for consistency.
"""

import random
from pathlib import Path
from typing import Set

class WordManager:
    """Manages word selection and validation."""

    def __init__(self, solution_path: str | None = None, guess_path: str | None = None):
        """Initialize word dictionaries from files or defaults."""
        data_dir = Path(__file__).parent.parent / "data"
        self._solution_path = solution_path or str(data_dir / "valid-solution-words.txt")
        self._guess_path = guess_path or str(data_dir / "valid-guess-words.txt")
        self._solution_words: Set[str] = set()
        self._guess_words: Set[str] = set()
        self._load_dictionaries()

    def _load_dictionaries(self) -> None:
        """Load word dictionaries from files or fall back to defaults."""
        try:
            # Load solution words
            with open(self._solution_path, 'r') as f:
                self._solution_words = {word.strip().upper() for word in f if len(word.strip()) == 5}

            # Load guess words
            with open(self._guess_path, 'r') as f:
                self._guess_words = {word.strip().upper() for word in f if len(word.strip()) == 5}

            # Solution words are also valid guesses
            self._guess_words.update(self._solution_words)

            if not self._solution_words or not self._guess_words:
                self._use_default_words()
        except (FileNotFoundError, ValueError):
            self._use_default_words()

    def _use_default_words(self) -> None:
        """Load minimal set of common 5-letter words as defaults."""
        self._solution_words = {
            "WORLD", "HELLO", "GAMES", "HAPPY", "SMILE", 
            "LAUGH", "DREAM", "PEACE", "LEARN", "THINK"
        }
        self._guess_words = self._solution_words.copy()

    def is_valid_word(self, word: str) -> bool:
        """True if word is in the valid guesses dictionary."""
        return word.upper() in self._guess_words

    def get_random_word(self) -> str:
        """Return a random word from solution dictionary."""
        return random.choice(list(self._solution_words))

    def add_word(self, word: str, is_solution: bool = False) -> bool:
        """Add a new 5-letter word to the appropriate dictionary.
        
        Returns False if:
        - Word is not 5 letters
        - Word already exists in target dictionary
        """
        # Validate word
        word = word.strip().upper()
        if len(word) != 5:
            return False

        # Handle solution words
        if is_solution:
            if word in self._solution_words:
                return False
            self._solution_words.add(word)
            self._guess_words.add(word)  # Solutions are valid guesses
            return True

        # Handle guess words
        if word in self._guess_words:
            return False
        self._guess_words.add(word)
        return True

    @property
    def solution_count(self) -> int:
        """Number of possible solution words."""
        return len(self._solution_words)

    @property
    def guess_count(self) -> int:
        """Number of valid guess words (includes solutions)."""
        return len(self._guess_words)
