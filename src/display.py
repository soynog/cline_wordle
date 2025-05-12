"""Display manager for handling game output with color support."""

from typing import List
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init()

class DisplayManager:
    """Manages the display formatting and rendering of the game state."""

    def __init__(self, use_color: bool = True):
        """Initialize the display manager.

        Args:
            use_color: Whether to use colored output (defaults to True)
        """
        self._use_color = use_color

    def format_guess(self, word: str, feedback: List[str]) -> str:
        """Format a guess with its feedback.

        Args:
            word: The guessed word
            feedback: List of feedback symbols for each letter

        Returns:
            str: Formatted string with colored letters or symbols
        """
        result = []
        for letter, symbol in zip(word, feedback):
            if self._use_color:
                if symbol == "✓":
                    # Green background for correct position
                    result.append(f"{Back.GREEN}{Fore.WHITE}{letter}{Style.RESET_ALL}")
                elif symbol == "○":
                    # Yellow background for wrong position
                    result.append(f"{Back.YELLOW}{Fore.BLACK}{letter}{Style.RESET_ALL}")
                else:
                    # Gray background for incorrect letter
                    result.append(f"{Back.LIGHTBLACK_EX}{Fore.WHITE}{letter}{Style.RESET_ALL}")
            else:
                # Non-color mode uses symbols
                result.append(f"{symbol}{letter}")
        
        return " ".join(result)

    def format_game_board(self, guesses: List[str], feedback: List[List[str]], max_attempts: int = 6) -> str:
        """Format the entire game board.

        Args:
            guesses: List of guessed words
            feedback: List of feedback for each guess
            max_attempts: Maximum number of attempts allowed

        Returns:
            str: Formatted game board string
        """
        lines = []
        for i in range(max_attempts):
            if i < len(guesses):
                lines.append(self.format_guess(guesses[i], feedback[i]))
            else:
                # Empty row for remaining attempts
                lines.append("_ " * 5)
        return "\n".join(lines)

    def format_keyboard(self, used_letters: dict) -> str:
        """Format the keyboard display showing used letters.

        Args:
            used_letters: Dictionary mapping letters to their status
                        ("✓" for correct, "○" for wrong position, "✗" for incorrect)

        Returns:
            str: Formatted keyboard string
        """
        keyboard = [
            "Q W E R T Y U I O P",
            " A S D F G H J K L",
            "  Z X C V B N M"
        ]
        
        result = []
        for row in keyboard:
            formatted_row = []
            for letter in row:
                if letter == " ":
                    formatted_row.append(" ")
                    continue
                
                status = used_letters.get(letter, None)
                if status is None:
                    # Unused letter
                    formatted_row.append(letter)
                elif self._use_color:
                    if status == "✓":
                        formatted_row.append(f"{Back.GREEN}{Fore.WHITE}{letter}{Style.RESET_ALL}")
                    elif status == "○":
                        formatted_row.append(f"{Back.YELLOW}{Fore.BLACK}{letter}{Style.RESET_ALL}")
                    else:
                        formatted_row.append(f"{Back.LIGHTBLACK_EX}{Fore.WHITE}{letter}{Style.RESET_ALL}")
                else:
                    formatted_row.append(f"{status}{letter}")
            
            result.append("".join(formatted_row))
        
        return "\n".join(result)

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        print("\033[H\033[J", end="")

    def show_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: The error message to display
        """
        print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

    def show_success(self, message: str) -> None:
        """Display a success message.

        Args:
            message: The success message to display
        """
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
