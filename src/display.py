"""Display manager for handling game output with color support.

Provides consistent formatting for:
- Game board with colored/symbolic feedback
- QWERTY keyboard showing letter statuses
- Error and success messages

Supports two display modes:
- Color mode: Uses colored backgrounds (default)
- Symbol mode: Uses ✓○✗ symbols as fallback
"""

from typing import List
from colorama import Fore, Back, Style, init

# Initialize colorama for cross-platform color support
init()

# Color combinations for different letter states
CORRECT_STYLE = f"{Back.GREEN}{Fore.WHITE}"
WRONG_POSITION_STYLE = f"{Back.YELLOW}{Fore.BLACK}"
INCORRECT_STYLE = f"{Back.LIGHTBLACK_EX}{Fore.WHITE}"

# Keyboard layout with proper indentation
KEYBOARD_LAYOUT = [
    "QWERTYUIOP",    # Row 1: No indent
    " ASDFGHJKL",    # Row 2: 1 space indent
    "  ZXCVBNM"      # Row 3: 2 space indent
]

class DisplayManager:
    """Manages the display formatting and rendering of the game state."""

    def __init__(self, use_color: bool = True):
        """Initialize the display manager.

        Args:
            use_color: Whether to use colored output (defaults to True)
        """
        self._use_color = use_color

    def format_guess(self, word: str, feedback: List[str]) -> str:
        """Format a guess with color/symbol feedback for each letter."""
        result = []
        for letter, symbol in zip(word, feedback):
            if self._use_color:
                if symbol == "✓":
                    result.append(f"{CORRECT_STYLE} {letter} {Style.RESET_ALL}")
                elif symbol == "○":
                    result.append(f"{WRONG_POSITION_STYLE} {letter} {Style.RESET_ALL}")
                else:
                    result.append(f"{INCORRECT_STYLE} {letter} {Style.RESET_ALL}")
            else:
                # Non-color mode uses symbols
                result.append(f"{symbol}{letter}")
        
        return "".join(result)

    def format_game_board(self, guesses: List[str], feedback: List[List[str]], max_attempts: int = 6) -> str:
        """Format game board with guesses and empty placeholder rows."""
        lines = []
        for i in range(max_attempts):
            if i < len(guesses):
                lines.append(self.format_guess(guesses[i], feedback[i]))
            else:
                # Empty row for remaining attempts - match width of colored squares
                empty_row = []
                for _ in range(5):
                    empty_row.append(" _ ")  # Three spaces total to match colored square width
                lines.append("".join(empty_row))
        return "\n".join(lines)

    def format_keyboard(self, used_letters: dict) -> str:
        """Format QWERTY keyboard with color/symbol status for each letter."""
        
        result = []
        for row in KEYBOARD_LAYOUT:
            formatted_row = []
            for letter in row:
                if letter == " ":
                    formatted_row.append(" ")
                    continue
                
                status = used_letters.get(letter, None)
                if status is None:
                    # Unused letter
                    formatted_row.append(f" {letter} ")
                elif self._use_color:
                    if status == "✓":
                        formatted_row.append(f"{CORRECT_STYLE} {letter} {Style.RESET_ALL}")
                    elif status == "○":
                        formatted_row.append(f"{WRONG_POSITION_STYLE} {letter} {Style.RESET_ALL}")
                    else:
                        formatted_row.append(f"{INCORRECT_STYLE} {letter} {Style.RESET_ALL}")
                else:
                    formatted_row.append(f"{status}{letter}")
            
            result.append("".join(formatted_row))
        
        return "\n".join(result)

    def clear_screen(self) -> None:
        """Clear terminal screen using ANSI escape sequence."""
        print("\033[H\033[J", end="")

    def show_error(self, message: str) -> None:
        """Display error message in red."""
        print(f"{Fore.RED}Error: {message}{Style.RESET_ALL}")

    def show_success(self, message: str) -> None:
        """Display success message in green."""
        print(f"{Fore.GREEN}{message}{Style.RESET_ALL}")
