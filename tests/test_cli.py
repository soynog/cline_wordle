"""Tests for the CLI module."""

import pytest
from src.cli import CLI

def test_cli_initialization():
    """Test CLI class initialization."""
    cli = CLI()
    assert cli._controller is not None
    assert cli._display is not None

def test_display_welcome(capsys):
    """Test welcome message display."""
    cli = CLI()
    cli.display_welcome()
    captured = capsys.readouterr()
    assert "Welcome to Command-Line Wordle!" in captured.out
    assert "Guess the WORDLE in 6 tries" in captured.out

def test_display_error(capsys):
    """Test error message display."""
    cli = CLI()
    test_message = "Invalid word"
    cli.display_error(test_message)
    captured = capsys.readouterr()
    assert f"Error: {test_message}" in captured.out
