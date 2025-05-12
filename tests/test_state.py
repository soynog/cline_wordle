"""Unit tests for game state management.

Tests state tracking functionality including:
- Game status transitions
- Statistics tracking
- State updates from guesses
"""

import pytest
from src.state import GameState, GameStatus

@pytest.fixture
def new_game():
    """Fixture providing a fresh game state."""
    return GameState.new_game("TESTS")

def test_get_statistics_new_game(new_game):
    """Test statistics for a newly created game.
    
    Should show:
    - 0 attempts used
    - Maximum attempts remaining
    - Not won
    """
    stats = new_game.get_statistics()
    assert stats["attempts"] == 0
    assert stats["remaining"] == 6
    assert stats["won"] is False

def test_get_statistics_after_guesses(new_game):
    """Test statistics after making some guesses.
    
    Should show:
    - Correct number of attempts used
    - Correct remaining attempts
    - Not won (game still in progress)
    """
    # Make two guesses
    new_game.update_with_guess("FIRST", ["✗", "✗", "✗", "✗", "✗"])
    new_game.update_with_guess("GUESS", ["✗", "✗", "✗", "✗", "✗"])
    
    stats = new_game.get_statistics()
    assert stats["attempts"] == 2
    assert stats["remaining"] == 4
    assert stats["won"] is False

def test_get_statistics_won_game(new_game):
    """Test statistics for a won game.
    
    Should show:
    - Correct number of attempts used
    - Remaining attempts preserved
    - Won status true
    """
    # Make two failed guesses
    new_game.update_with_guess("FIRST", ["✗", "✗", "✗", "✗", "✗"])
    new_game.update_with_guess("GUESS", ["✗", "✗", "✗", "✗", "✗"])
    # Win on third guess
    new_game.update_with_guess("TESTS", ["✓", "✓", "✓", "✓", "✓"])
    
    stats = new_game.get_statistics()
    assert stats["attempts"] == 3
    assert stats["remaining"] == 3
    assert stats["won"] is True

def test_get_statistics_lost_game(new_game):
    """Test statistics for a lost game.
    
    Should show:
    - Maximum attempts used
    - No attempts remaining
    - Not won
    """
    # Make 6 failed guesses
    for _ in range(6):
        new_game.update_with_guess("WRONG", ["✗", "✗", "✗", "✗", "✗"])
    
    stats = new_game.get_statistics()
    assert stats["attempts"] == 6
    assert stats["remaining"] == 0
    assert stats["won"] is False
