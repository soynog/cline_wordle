"""Tests for the game controller module."""

import pytest
from src.controller import GameController
from unittest.mock import Mock

@pytest.fixture
def mock_word_manager():
    """Create a mock word manager."""
    manager = Mock()
    manager.get_random_word.return_value = "TESTS"
    manager.is_valid_word.return_value = True
    return manager

@pytest.fixture
def mock_display_manager():
    """Create a mock display manager."""
    return Mock()

@pytest.fixture
def controller(mock_word_manager, mock_display_manager):
    """Create a game controller with mock dependencies."""
    return GameController(mock_word_manager, mock_display_manager)

def test_controller_initialization(controller):
    """Test controller initialization."""
    assert controller._state is None
    assert controller._word_manager is not None
    assert controller._display_manager is not None

def test_start_game(controller, mock_word_manager):
    """Test starting a new game."""
    controller.start_game()
    assert controller.target_word == "TESTS"
    assert len(controller.guesses) == 0
    assert len(controller.feedback) == 0
    assert not controller.game_won
    mock_word_manager.get_random_word.assert_called_once()

def test_make_guess_valid_word(controller):
    """Test making a valid guess."""
    controller.start_game()  # Sets target word to "TESTS"
    success, message = controller.make_guess("TRAIN")
    assert success
    assert message == ""
    assert len(controller.guesses) == 1
    assert len(controller.feedback) == 1
    assert not controller.game_won

def test_make_guess_winning_word(controller):
    """Test making a winning guess."""
    controller.start_game()  # Sets target word to "TESTS"
    success, message = controller.make_guess("TESTS")
    assert success
    assert message == ""
    assert controller.game_won
    assert controller.guesses == ["TESTS"]

def test_make_guess_invalid_length(controller):
    """Test making a guess with invalid length."""
    controller.start_game()
    success, message = controller.make_guess("TOO")
    assert not success
    assert "must be 5 letters" in message
    assert len(controller.guesses) == 0

def test_make_guess_invalid_word(controller, mock_word_manager):
    """Test making a guess with an invalid word."""
    mock_word_manager.is_valid_word.return_value = False
    controller.start_game()
    success, message = controller.make_guess("XXXXX")
    assert not success
    assert "Not a valid word" in message
    assert len(controller.guesses) == 0
