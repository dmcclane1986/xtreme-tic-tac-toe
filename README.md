# Xtreme Tic-Tac-Toe

A Python implementation of Ultimate Tic-Tac-Toe (also known as Meta Tic-Tac-Toe or Strategic Tic-Tac-Toe) using Tkinter for the GUI.

## Game Description

Xtreme Tic-Tac-Toe is a complex variant of the classic Tic-Tac-Toe game. The game board consists of nine smaller Tic-Tac-Toe boards arranged in a 3x3 grid, creating a larger Tic-Tac-Toe board.

## Rules

1. **Basic Setup**
   - The game board consists of 9 smaller Tic-Tac-Toe boards arranged in a 3x3 grid
   - Two players take turns, using 'X' and 'O' markers
   - The goal is to win three small boards in a row (horizontally, vertically, or diagonally)

2. **Game Flow**
   - The first player can place their marker anywhere on any of the small boards
   - The position where a player places their marker determines which board the next player must play in
   - For example, if a player places their marker in the top-right square of any small board, the next player must play in the top-right small board

3. **Special Rules**
   - If a player is sent to a board that is already won or filled (drawn), they can play in any available board
   - When this happens, "Free Choice" will be displayed, indicating the player can choose any available board
   - The active board where the current player must play is highlighted in yellow

4. **Winning Conditions**
   - **Small Boards**: Win by getting three markers in a row (horizontally, vertically, or diagonally)
   - **Main Game**: Win by winning three small boards in a row (horizontally, vertically, or diagonally)
   - If all boards are filled without a winner, the game ends in a tie

5. **Visual Indicators**
   - Won boards display the winner's symbol ('X' or 'O') in large red text
   - Drawn boards display 'T' in the center
   - The active board is highlighted in yellow
   - The game status is displayed at the top of the window

## How to Play

1. **Starting the Game**
   - Run the Python script
   - The first player ('X') can place their marker anywhere
   - Follow the prompts at the top of the window for whose turn it is and where you can play

2. **Controls**
   - Click any valid square to place your marker
   - Use the "Reset Game" button to start a new game at any time

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dmcclane1986/xtreme-tic-tac-toe.git
```

2. Navigate to the game directory:
```bash
cd xtreme-tic-tac-toe
```

3. Run the game:
```bash
python3 xtreme-tic-tac-toe.py
```
