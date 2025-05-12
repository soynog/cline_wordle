"""Tests for the word manager module."""

import pytest
from src.word_manager import WordManager
from pathlib import Path
import tempfile
import os

@pytest.fixture
def temp_solution_dictionary():
    """Create a temporary solution words file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("HELLO\nWORLD\nTESTS\nLIGHT\nBREAK\n")
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)

@pytest.fixture
def temp_guess_dictionary():
    """Create a temporary guess words file."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("HELLO\nWORLD\nTESTS\nLIGHT\nBREAK\nEXTRA\nGUESS\nWORDS\n")
        temp_path = f.name
    yield temp_path
    os.unlink(temp_path)

@pytest.fixture
def word_manager(temp_solution_dictionary, temp_guess_dictionary):
    """Create a WordManager instance with test dictionaries."""
    return WordManager(temp_solution_dictionary, temp_guess_dictionary)

def test_word_manager_initialization(word_manager):
    """Test WordManager initialization."""
    assert word_manager.solution_count == 5
    assert word_manager.guess_count == 8
    assert isinstance(word_manager._solution_words, set)
    assert isinstance(word_manager._guess_words, set)

def test_word_manager_default_words():
    """Test WordManager with default word lists."""
    manager = WordManager("nonexistent_file.txt", "nonexistent_file.txt")
    assert manager.solution_count > 0
    assert manager.guess_count > 0
    assert all(len(word) == 5 for word in manager._solution_words)
    assert all(len(word) == 5 for word in manager._guess_words)

def test_is_valid_word(word_manager):
    """Test word validation."""
    # Test solution words
    assert word_manager.is_valid_word("HELLO")
    assert word_manager.is_valid_word("hello")  # Should be case-insensitive
    
    # Test guess-only words
    assert word_manager.is_valid_word("EXTRA")
    assert word_manager.is_valid_word("extra")  # Should be case-insensitive
    
    # Test invalid words
    assert not word_manager.is_valid_word("INVALID")
    assert not word_manager.is_valid_word("HI")  # Too short
    assert not word_manager.is_valid_word("TOOLONG")  # Too long

def test_get_random_word(word_manager):
    """Test random word selection."""
    word = word_manager.get_random_word()
    assert word in word_manager._solution_words
    assert word in word_manager._guess_words  # Solution words should be in guess words too
    assert len(word) == 5
    assert word.isupper()

def test_add_word(word_manager):
    """Test adding new words."""
    initial_solution_count = word_manager.solution_count
    initial_guess_count = word_manager.guess_count
    
    # Test adding solution word
    assert word_manager.add_word("PAINT", is_solution=True)
    assert word_manager.solution_count == initial_solution_count + 1
    assert word_manager.guess_count == initial_guess_count + 1  # Should be added to both sets
    assert word_manager.is_valid_word("PAINT")
    
    # Test adding guess word
    assert word_manager.add_word("CRANE")  # is_solution defaults to False
    assert word_manager.solution_count == initial_solution_count + 1  # Shouldn't change
    assert word_manager.guess_count == initial_guess_count + 2
    assert word_manager.is_valid_word("CRANE")

    # Test adding invalid words
    assert not word_manager.add_word("WORLD", is_solution=True)  # Already exists
    assert not word_manager.add_word("EXTRA")  # Already exists in guess words
    assert not word_manager.add_word("LONG")  # Too short
    assert not word_manager.add_word("TOOLONG")  # Too long
    assert word_manager.solution_count == initial_solution_count + 1
    assert word_manager.guess_count == initial_guess_count + 2

def test_load_empty_dictionaries():
    """Test loading empty dictionaries."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f1, \
         tempfile.NamedTemporaryFile(mode='w', delete=False) as f2:
        solution_path = f1.name
        guess_path = f2.name
    
    try:
        manager = WordManager(solution_path, guess_path)
        # Should fall back to default words
        assert manager.solution_count > 0
        assert manager.guess_count > 0
        assert all(len(word) == 5 for word in manager._solution_words)
        assert all(len(word) == 5 for word in manager._guess_words)
    finally:
        os.unlink(solution_path)
        os.unlink(guess_path)

def test_case_consistency(word_manager):
    """Test that words are stored and compared in uppercase."""
    # Test with solution word
    assert word_manager.add_word("lower", is_solution=True)
    assert word_manager.is_valid_word("LOWER")
    assert word_manager.is_valid_word("lower")
    assert word_manager.is_valid_word("LoWeR")
    assert "LOWER" in word_manager._solution_words
    assert "LOWER" in word_manager._guess_words
    assert "lower" not in word_manager._solution_words
    assert "lower" not in word_manager._guess_words

    # Test with guess word
    assert word_manager.add_word("upper")
    assert word_manager.is_valid_word("UPPER")
    assert word_manager.is_valid_word("upper")
    assert "UPPER" in word_manager._guess_words
    assert "UPPER" not in word_manager._solution_words
    assert "upper" not in word_manager._guess_words

def test_solution_words_are_valid_guesses(word_manager):
    """Test that solution words are automatically valid guess words."""
    # Add a new solution word
    assert word_manager.add_word("SMART", is_solution=True)
    
    # Should be in both sets
    assert "SMART" in word_manager._solution_words
    assert "SMART" in word_manager._guess_words
    
    # Should be valid for guessing
    assert word_manager.is_valid_word("SMART")
