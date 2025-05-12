"""Tests for the display manager module."""

import pytest
from src.display import DisplayManager
from colorama import Fore, Back, Style
from tests.helpers import strip_color_codes

@pytest.fixture
def display_manager():
    """Create a DisplayManager instance."""
    return DisplayManager()

@pytest.fixture
def display_manager_no_color():
    """Create a DisplayManager instance with color disabled."""
    return DisplayManager(use_color=False)

def test_display_manager_initialization(display_manager):
    """Test DisplayManager initialization."""
    assert display_manager._use_color is True

def test_format_guess_with_color(display_manager):
    """Test guess formatting with color."""
    word = "TESTS"
    feedback = ["✓", "○", "✗", "○", "✓"]
    formatted = display_manager.format_guess(word, feedback)
    
    # Should contain color codes
    assert Back.GREEN in formatted
    assert Back.YELLOW in formatted
    assert Back.LIGHTBLACK_EX in formatted
    assert Style.RESET_ALL in formatted
    
    # Should contain all letters
    for letter in word:
        assert letter in formatted

def test_format_guess_without_color(display_manager_no_color):
    """Test guess formatting without color."""
    word = "TESTS"
    feedback = ["✓", "○", "✗", "○", "✓"]
    formatted = display_manager_no_color.format_guess(word, feedback)
    
    # Should not contain color codes
    assert Back.GREEN not in formatted
    assert Back.YELLOW not in formatted
    assert Back.LIGHTBLACK_EX not in formatted
    assert Style.RESET_ALL not in formatted
    
    # Should contain symbols and letters
    for symbol, letter in zip(feedback, word):
        assert f"{symbol}{letter}" in formatted

def test_format_game_board(display_manager):
    """Test game board formatting."""
    guesses = ["FIRST", "SECOND"]
    feedback = [
        ["✓", "○", "✗", "○", "✓"],
        ["✓", "✓", "✓", "✗", "○"]
    ]
    
    formatted = display_manager.format_game_board(guesses, feedback)
    
    # Should be multiple lines
    assert "\n" in formatted
    
    # Should contain empty rows
    assert "_ " in formatted

def test_format_keyboard(display_manager):
    """Test keyboard formatting."""
    used_letters = {
        "T": "✓",  # Correct
        "E": "○",  # Wrong position
        "S": "✗"   # Not in word
    }
    
    formatted = display_manager.format_keyboard(used_letters)
    
    # Should be multiple lines
    assert "\n" in formatted
    
    # Should contain all keyboard rows with proper structure
    rows = formatted.split('\n')
    assert len(rows) == 3  # Should have 3 rows
    
    # Check that each row contains the correct letters (ignoring color codes)
    clean_rows = [strip_color_codes(row) for row in rows]
    assert all(c in clean_rows[0] for c in "QWERTYUIOP")
    assert all(c in clean_rows[1] for c in "ASDFGHJKL")
    assert all(c in clean_rows[2] for c in "ZXCVBNM")

def test_show_error(display_manager, capsys):
    """Test error message display."""
    message = "Test error"
    display_manager.show_error(message)
    captured = capsys.readouterr()
    assert message in captured.out
    assert Fore.RED in captured.out

def test_show_success(display_manager, capsys):
    """Test success message display."""
    message = "Test success"
    display_manager.show_success(message)
    captured = capsys.readouterr()
    assert message in captured.out
    assert Fore.GREEN in captured.out
