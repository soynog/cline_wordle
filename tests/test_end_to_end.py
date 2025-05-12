"""End-to-end tests for the Wordle game.

These tests verify the complete application from the user's perspective,
simulating actual gameplay through the CLI interface.
"""

import pytest
from unittest.mock import patch, Mock
from src.cli import CLI
from tests.helpers import strip_color_codes

class TestGameE2E:
    @pytest.fixture
    def cli_setup(self):
        """Set up CLI with controlled input/output."""
        cli = CLI()
        # Patch clear_screen to do nothing to avoid ANSI escape codes
        cli._display.clear_screen = Mock()
        return cli

    def test_game_startup(self, cli_setup, capsys):
        """Test game startup and welcome message.
        
        Verifies that:
        - Welcome message is displayed
        - Game instructions are shown
        - Initial empty game board is displayed
        """
        with patch('src.word_manager.WordManager.get_random_word', return_value='TESTS'):
            # Display welcome message
            cli_setup.display_welcome()
            
            # Start game and show initial state
            cli_setup._controller.start_game()
            cli_setup.display_game_state()
            
            # Capture and clean output
            captured = capsys.readouterr()
            clean_output = strip_color_codes(captured.out)
            
            # Verify welcome message
            assert "Welcome to Command-Line Wordle!" in clean_output
            assert "Guess the WORDLE in 6 tries" in clean_output
            assert "Each guess must be a valid 5-letter word" in clean_output
            
            # Verify game board setup
            assert "Wordle" in clean_output
            assert "Keyboard" in clean_output
            
            # Verify empty game board (5 rows of 5 empty spaces)
            assert clean_output.count(" _ ") == 30  # 6 rows * 5 spaces

    def test_single_guess(self, cli_setup, capsys):
        """Test making a single guess.
        
        Verifies that:
        - User can input a guess
        - Guess is displayed on the board
        - Feedback is shown correctly
        - Keyboard is updated
        """
        with patch('src.word_manager.WordManager.get_random_word', return_value='TESTS'):
            # Start game
            cli_setup._controller.start_game()
            cli_setup.display_game_state()
            captured = capsys.readouterr()  # Clear initial output
            
            # Make a guess
            success, _ = cli_setup._controller.make_guess('TRAIN')
            assert success
            
            # Display updated state
            cli_setup.display_game_state()
            captured = capsys.readouterr()  # Get output after guess
            clean_output = strip_color_codes(captured.out)
            
            # Verify guess appears on board
            assert 'T' in clean_output  # First letter is correct
            assert 'R' in clean_output  # Second letter is wrong
            assert 'A' in clean_output  # Third letter is wrong
            assert 'I' in clean_output  # Fourth letter is wrong
            assert 'N' in clean_output  # Fifth letter is wrong
            
            # Verify remaining empty rows
            assert clean_output.count(" _ ") == 25  # 5 rows * 5 spaces
            
            # Verify keyboard shows used letters
            keyboard_section = clean_output[clean_output.find("Keyboard"):]
            for letter in 'TRAIN':
                assert letter in keyboard_section

    def test_winning_game(self, cli_setup, capsys):
        """Test winning the game by guessing the correct word.
        
        Verifies that:
        - Correct guess is recognized
        - Win message is displayed
        - Game board shows winning state
        - Game ends after win
        """
        with patch('src.word_manager.WordManager.get_random_word', return_value='TESTS'):
            # Start game
            cli_setup._controller.start_game()
            cli_setup.display_game_state()
            captured = capsys.readouterr()  # Clear initial output
            
            # Make winning guess
            success, _ = cli_setup._controller.make_guess('TESTS')
            assert success
            
            # Display final state
            cli_setup.display_game_state()
            cli_setup.display_result(cli_setup._controller.game_won, cli_setup._controller.target_word)
            captured = capsys.readouterr()
            clean_output = strip_color_codes(captured.out)
            
            # Verify winning state
            assert 'TESTS' in clean_output
            assert "Result: Won!" in clean_output
            assert "Congratulations" in clean_output
            
            # Verify game ended (should not accept more guesses)
            success, message = cli_setup._controller.make_guess('TRAIN')
            assert not success
            assert "already over" in message.lower()

    def test_losing_game(self, cli_setup, capsys):
        """Test losing the game after 6 incorrect guesses.
        
        Verifies that:
        - All 6 guesses are processed
        - Loss message is displayed
        - Correct answer is revealed
        - Game ends after loss
        """
        with patch('src.word_manager.WordManager.get_random_word', return_value='TESTS'):
            # Start game
            cli_setup._controller.start_game()
            cli_setup.display_game_state()
            captured = capsys.readouterr()  # Clear initial output
            
            # Make 6 incorrect guesses
            test_words = ['TRAIN', 'CLOUD', 'HAPPY', 'WORLD', 'BRAIN', 'SMILE']
            for word in test_words:
                success, _ = cli_setup._controller.make_guess(word)
                assert success
                cli_setup.display_game_state()
                captured = capsys.readouterr()
            
            # Display final state with result
            cli_setup.display_game_state()
            cli_setup.display_result(cli_setup._controller.game_won, cli_setup._controller.target_word)
            captured = capsys.readouterr()
            clean_output = strip_color_codes(captured.out)
            
            # Verify final state
            assert "Result: Lost" in clean_output
            assert "Game Over" in clean_output
            assert "TESTS" in clean_output  # Answer should be revealed
            
            # Verify game ended (should not accept more guesses)
            success, message = cli_setup._controller.make_guess('FINAL')
            assert not success
            assert "already over" in message.lower()

    def test_invalid_input_handling(self, cli_setup, capsys):
        """Test handling of invalid user input.
        
        Verifies that:
        - Too short words are rejected
        - Too long words are rejected
        - Non-alphabetic input is rejected
        - Invalid words are rejected
        - Error messages are displayed
        """
        with patch('src.word_manager.WordManager.get_random_word', return_value='TESTS'), \
             patch.object(cli_setup._controller._word_manager, 'is_valid_word', return_value=False):
            
            # Start game
            cli_setup._controller.start_game()
            cli_setup.display_game_state()
            captured = capsys.readouterr()  # Clear initial output
            
            # Test too short word
            success, message = cli_setup._controller.make_guess('CAT')
            assert not success
            cli_setup.display_error(message)
            captured = capsys.readouterr()
            assert "5 letters" in captured.out
            
            # Test too long word
            success, message = cli_setup._controller.make_guess('CATDOG')
            assert not success
            cli_setup.display_error(message)
            captured = capsys.readouterr()
            assert "5 letters" in captured.out
            
            # Test non-alphabetic input
            success, message = cli_setup._controller.make_guess('CAT12')
            assert not success
            cli_setup.display_error(message)
            captured = capsys.readouterr()
            assert "Error" in captured.out
            
            # Test invalid word
            success, message = cli_setup._controller.make_guess('XXXXX')
            assert not success
            cli_setup.display_error(message)
            captured = capsys.readouterr()
            assert "Not a valid word" in captured.out
            
            # Verify game board is unchanged
            cli_setup.display_game_state()
            captured = capsys.readouterr()
            clean_output = strip_color_codes(captured.out)
            assert clean_output.count(" _ ") == 30  # Still all empty
