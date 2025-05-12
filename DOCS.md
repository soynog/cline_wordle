# Command-Line Wordle User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [How to Play](#how-to-play)
4. [Game Rules](#game-rules)
5. [Visual Feedback](#visual-feedback)
6. [Examples](#examples)
7. [Tips and Strategies](#tips-and-strategies)
8. [Troubleshooting](#troubleshooting)

## Introduction

Command-Line Wordle is a terminal-based implementation of the popular word-guessing game. The objective is to guess a five-letter word within six attempts. After each guess, you receive feedback showing which letters are correct and in the right position, which letters are in the word but in the wrong position, and which letters are not in the word at all.

## Installation

1. Ensure you have Python 3.8 or higher installed:
   ```bash
   python --version
   ```

2. Clone the repository and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd wordle
   ```

3. Create and activate a virtual environment:
   ```bash
   # On Unix/macOS
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Start the game:
   ```bash
   python -m src.cli
   ```

2. You'll see the welcome screen with an empty game board and keyboard display.

3. Type a 5-letter word and press Enter to make a guess.

4. After each guess, you'll see:
   - The word you guessed with color-coded feedback
   - Updated keyboard showing used letters
   - Remaining attempts

5. Keep guessing until you either:
   - Correctly guess the word (win)
   - Use all 6 attempts without guessing the word (lose)

6. After the game ends, you'll be asked if you want to play again.

## Game Rules

1. Each guess must be a valid 5-letter word
2. You have 6 attempts to guess the word
3. The same letter can appear multiple times in a word
4. All letters must be in English alphabet (A-Z)
5. Guesses are not case-sensitive
6. Words can include repeated letters

## Visual Feedback

After each guess, you receive feedback in the form of colored squares (or symbols in non-color mode):

### Color Mode
- 🟩 Green: Letter is correct and in the right position
- 🟨 Yellow: Letter is in the word but in the wrong position
- ⬛ Gray: Letter is not in the word

### Non-Color Mode
- ✓: Letter is correct and in the right position
- ○: Letter is in the word but in the wrong position
- ✗: Letter is not in the word

The keyboard display at the bottom of the screen also updates to show:
- Which letters you've used
- Their status (correct, wrong position, or not in word)
- Remaining unused letters

## Examples

### Example 1: Winning Game
```
Target word: LIGHT
Guess 1: STARE ⬛🟨⬛⬛⬛ (T is in word, wrong position)
Guess 2: THINK 🟨⬛🟨🟨⬛ (T, I, H in word, wrong positions)
Guess 3: LIGHT 🟩🟩🟩🟩🟩 (All correct - You win!)
```

### Example 2: Losing Game
```
Target word: CRANE
Guess 1: STARE ⬛⬛🟨🟩⬛
Guess 2: BRAKE ⬛🟩🟨🟩⬛
Guess 3: GRADE ⬛🟩🟨🟩⬛
Guess 4: TRACE ⬛🟩🟨🟩⬛
Guess 5: FRAME ⬛🟩🟨🟩⬛
Guess 6: DRAPE ⬛🟩🟨🟩⬛
Game Over! The word was: CRANE
```

## Tips and Strategies

1. Start with words that contain common letters (E, A, R, I, O, T, N, S)
2. Use your first guess to eliminate as many common letters as possible
3. Pay attention to repeated letters - they're allowed!
4. Use the keyboard display to track which letters you haven't tried
5. If you find a correct letter (green), keep it in the same position for future guesses
6. Try to use different letters in each guess until you find some matches

## Troubleshooting

### Common Issues and Solutions

1. **Game doesn't start**
   - Ensure Python 3.8+ is installed
   - Verify virtual environment is activated
   - Check all dependencies are installed

2. **Colors not displaying correctly**
   - Ensure your terminal supports ANSI colors
   - Try updating your terminal application
   - The game will automatically fall back to symbol mode if color support is unavailable

3. **Invalid word errors**
   - Ensure word is exactly 5 letters
   - Check that all characters are letters (A-Z)
   - Verify the word is in the game's dictionary

4. **Performance issues**
   - Ensure you're running the latest version
   - Check system resources
   - Try restarting the game

### Error Messages

- "Guess must be 5 letters": Your guess was too short or too long
- "Not a valid word": The word isn't in the game's dictionary
- "Game is already over": You're trying to guess after the game has ended

For additional help or to report issues, please visit the project's GitHub repository.
