"""Integration tests for the Wordle game.

These tests verify that different components of the system work together correctly.
They focus on testing the interactions between:
- GameController and WordManager
- GameController and DisplayManager
- State management across components
- Feedback generation and processing
"""

import pytest
from unittest.mock import patch
from src.cli import CLI
from src.controller import GameController
from src.word_manager import WordManager
from src.display import DisplayManager
from tests.helpers import strip_color_codes

@pytest.fixture
def game_setup():
    """Set up a complete game instance with real components."""
    cli = CLI()  # CLI creates its own components
    return {
        'cli': cli,
        'controller': cli._controller,
        'word_manager': cli._controller._word_manager,
        'display_manager': cli._display
    }

def test_word_manager_controller_integration(game_setup):
    """Test integration between WordManager and GameController."""
    controller = game_setup['controller']
    
    with patch.object(game_setup['word_manager'], 'get_random_word', return_value='TESTS'):
        controller.start_game()
        
        # Make some incorrect guesses first
        success, _ = controller.make_guess('TRAIN')
        assert success
        success, _ = controller.make_guess('SPEAK')
        assert success
        
        # Verify game state after incorrect guesses
        assert len(controller.guesses) == 2
        assert not controller.game_won
        assert controller.target_word == 'TESTS'
        
        # Make winning guess
        success, _ = controller.make_guess('TESTS')
        
        # Verify win condition
        assert success
        assert controller.game_won
        assert len(controller.guesses) == 3
        assert controller.guesses[-1] == 'TESTS'

def test_display_controller_integration(game_setup):
    """Test integration between DisplayManager and GameController."""
    controller = game_setup['controller']
    display = game_setup['display_manager']
    
    with patch.object(game_setup['word_manager'], 'get_random_word', return_value='TESTS'):
        controller.start_game()
        
        # Make a guess and verify display
        success, _ = controller.make_guess('TRAIN')
        assert success
        
        # Verify display shows correct feedback
        game_board = display.format_game_board(controller.guesses, controller.feedback)
        clean_board = strip_color_codes(game_board)
        
        # T should be correct (✓), R and N should be wrong (✗)
        assert ' T ' in clean_board  # First letter is T
        assert ' R ' in clean_board  # Second letter is R
        assert ' N ' in clean_board  # Last letter is N

def test_word_validation_integration(game_setup):
    """Test integration of word validation between WordManager and GameController."""
    controller = game_setup['controller']
    word_manager = game_setup['word_manager']
    
    controller.start_game()
    
    # Test invalid word validation
    with patch.object(word_manager, 'is_valid_word', return_value=False):
        success, message = controller.make_guess('XXXXX')
        assert not success
        assert "Not a valid word" in message
    
    # Test valid word validation
    with patch.object(word_manager, 'is_valid_word', return_value=True):
        success, message = controller.make_guess('TESTS')
        assert success

def test_feedback_generation_integration(game_setup):
    """Test integration of feedback generation between components."""
    controller = game_setup['controller']
    
    with patch.object(game_setup['word_manager'], 'get_random_word', return_value='TESTS'):
        controller.start_game()
        
        # Make a guess with some correct letters
        success, _ = controller.make_guess('TREAD')
        assert success
        
        feedback = controller.feedback[-1]
        # T should be correct and in position (✓)
        assert feedback[0] == "✓"
        # E should be correct but wrong position (○)
        assert feedback[2] == "○"
        
        # Make winning guess
        success, _ = controller.make_guess('TESTS')
        assert success
        
        feedback = controller.feedback[-1]
        # All letters should be correct (all ✓)
        assert all(mark == "✓" for mark in feedback)

def test_state_management_integration(game_setup):
    """Test state management integration across components."""
    controller = game_setup['controller']
    
    with patch.object(game_setup['word_manager'], 'get_random_word', return_value='TESTS'):
        controller.start_game()
        
        # After game start
        assert controller.target_word == 'TESTS'
        assert len(controller.guesses) == 0
        assert not controller.game_won
        
        # After first guess
        success, _ = controller.make_guess('TRAIN')
        assert success
        assert len(controller.guesses) == 1
        assert not controller.game_won
        
        # After winning guess
        success, _ = controller.make_guess('TESTS')
        assert success
        assert len(controller.guesses) == 2
        assert controller.game_won

def test_component_event_handling(game_setup):
    """Test event handling and communication between components."""
    controller = game_setup['controller']
    display = game_setup['display_manager']
    
    with patch.object(game_setup['word_manager'], 'get_random_word', return_value='TESTS'):
        controller.start_game()
        
        # Make guesses and verify display updates
        success, _ = controller.make_guess('TRAIN')
        assert success
        
        # Verify display shows guess and feedback
        game_board = display.format_game_board(controller.guesses, controller.feedback)
        clean_board = strip_color_codes(game_board)
        assert ' T ' in clean_board  # First letter is T
        
        # Verify keyboard shows used letters
        keyboard = display.format_keyboard(controller.used_letters)
        clean_keyboard = strip_color_codes(keyboard)
        for letter in 'TRAIN':
            assert letter in clean_keyboard
