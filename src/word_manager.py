"""Word management module for handling word selection and validation."""

import random
from pathlib import Path
from typing import Set

class WordManager:
    """Manages word selection and validation."""

    def __init__(self, solution_path: str = None, guess_path: str = None):
        """Initialize the word manager.

        Args:
            solution_path: Path to the solution words file. If None, uses default.
            guess_path: Path to the valid guess words file. If None, uses default.
        """
        data_dir = Path(__file__).parent.parent / "data"
        self._solution_path = solution_path or str(data_dir / "valid-solution-words.txt")
        self._guess_path = guess_path or str(data_dir / "valid-guess-words.txt")
        self._solution_words: Set[str] = set()
        self._guess_words: Set[str] = set()
        self._load_dictionaries()

    def _load_dictionaries(self) -> None:
        """Load both solution and guess word dictionaries.

        All words are converted to uppercase for consistency.
        If either file fails to load, falls back to default words.
        """
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
        """Load default word sets when dictionary files are empty or not found."""
        self._solution_words = {
            "WORLD", "HELLO", "GAMES", "HAPPY", "SMILE", 
            "LAUGH", "DREAM", "PEACE", "LEARN", "THINK"
        }
        self._guess_words = self._solution_words.copy()

    def is_valid_word(self, word: str) -> bool:
        """Check if a word is valid for guessing.

        Args:
            word: The word to validate

        Returns:
            bool: True if the word is in either dictionary
        """
        return word.upper() in self._guess_words

    def get_random_word(self) -> str:
        """Get a random word from the solution dictionary.

        Returns:
            str: A random 5-letter word in uppercase
        """
        return random.choice(list(self._solution_words))

    def add_word(self, word: str, is_solution: bool = False) -> bool:
        """Add a new word to the appropriate dictionary.

        Args:
            word: The word to add (must be 5 letters)
            is_solution: If True, add to solution words. Otherwise, add to guess words.

        Returns:
            bool: True if the word was added successfully
        """
        word = word.strip().upper()
        if len(word) != 5:
            return False

        if is_solution:
            if word in self._solution_words:
                return False
            self._solution_words.add(word)
            self._guess_words.add(word)  # Solution words are also valid guesses
        else:
            if word in self._guess_words:
                return False
            self._guess_words.add(word)
        return True

    @property
    def solution_count(self) -> int:
        """Get the number of possible solution words.

        Returns:
            int: Number of solution words
        """
        return len(self._solution_words)

    @property
    def guess_count(self) -> int:
        """Get the number of valid guess words.

        Returns:
            int: Number of valid guess words
        """
        return len(self._guess_words)
