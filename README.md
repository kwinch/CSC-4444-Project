# CSC-4444-Project
An AI that can plays 3D Connect Four against a player.

### How to Run: 
Download and unzip the folder. Navigate to the file "game_interface.py" and run it to start the game. 

### Requirements: 
PyOpenGL installed. In the terminal, run: 
  pip install PyOpenGL

PyGame installed. In the terminal, run: 
  pip install pygame

### Controls: 
Use WASD to rotate the display. 
Use the arrow keys to select a peg, highlighted in blue.
Use the "enter" key to place a piece on the selected peg. The player will place red pieces, the AI will place yellow pieces. 


## Files

game_state.py  
  -Contains the Connect43D class and all game rules.  
main.py  
  -Simple terminal runner for testing the game manually.  
tests.py  
  -Basic assertion tests for the game logic.  
game_ab.py
  -Alpha-Beta pruning tree.
game_minimax.py
  -Minimax algorithm.
game_interface.py
  -3D interface for playing the game.

----------------------------------------------------------------
### Max Duet Game Functions Notes and Integration:

# 3D Connect 4 Backend

This contains the backend game logic for a 3D Connect 4 game.  
It is designed to be used later by an AI agent and a graphical interface.

## Features

- 3D board representation
- Move validation
- Gravity-based piece placement
- Win detection in all 3D directions
- Draw detection
- Board reset
- Board cloning for future AI/search use
- Undo support

## Board Representation

The board is stored as:

```python
board[z][y][x]
```

## Files

game_state.py  
  -Contains the Connect43D class and all game rules.  
main.py  
  -Simple terminal runner for testing the game manually.  
tests.py  
  -Basic assertion tests for the game logic.  

## Usage

### Make sure all files are in the same folder, then run:

```python
python main.py
```

### To run the tests:

```python
python tests.py
```

## How to Play in the Terminal

### When running main.py, enter moves in this format:

```python
x y
```

### Example:

```python
3 2
```

### This means:

column 3
row 2

### Game States
winner = 0 = game is still running
winner = 1 = player 1 wins
winner = 2 = player 2 wins
winner = -1 = draw


## Main Methods
```python
make_move(x, y, player=None)

Places a piece in the selected stack.

is_valid_move(x, y)

Checks whether a move can be made.

get_legal_moves()

Returns all available (x, y) moves.

check_win_from_position(x, y, z, player)

Checks whether the last move created a win.

reset()

Clears the board and starts a new game.

clone()

Creates a copy of the current game state.

undo_move()

Removes the most recent move.
```
----------------------------------------------------------------
