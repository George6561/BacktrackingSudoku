# Backtracking Sudoku Solver

This is a desktop GUI application built in Python that solves standard 9x9 Sudoku puzzles using a backtracking algorithm. It includes an interactive interface that lets you click, type, solve, and reset puzzles visually.

---

## Features

- Simple and clean graphical user interface using Tkinter
- Clickable Sudoku grid with keyboard navigation
- Supports number input via keyboard
- Highlights the currently selected cell
- Solve button uses a backtracking algorithm to find the solution
- Clear button resets the board instantly
- Uses image-based rendering for the grid and number tiles

---

## How to Run

1. Make sure you have Python 3 installed.

2. Install the required library:

   ```bash
   pip install pillow
   ```

3. Clone the repository:

   ```bash
   git clone https://github.com/George6561/BacktrackingSudoku.git
   cd BacktrackingSudoku
   ```

4. Run the application:

   ```bash
   python main.py
   ```

---

## File Overview

- `main.py` – Entry point that launches the GUI
- `sudoku_gui.py` – Handles user interface, input, and display logic
- `sudoku_board.py` – Contains the Sudoku board and solving algorithm
- `.png` and `.jpg` files – Assets for UI rendering (numbers, buttons, board)

---

## How It Works

The solving logic is based on a recursive backtracking approach. It tries placing digits 1 through 9 in each empty cell, validating the placement against Sudoku rules. If a number causes a conflict later on, the algorithm backtracks and tries the next one.

The GUI is built with Tkinter. Users can interact with the board by clicking cells and using the keyboard. The board can be reset at any time, and solutions are computed when the solve button is pressed.

---

## License

This project is licensed under the MIT License.  
See the `LICENSE` file for details.

---

## Author

George Miller  
[https://github.com/George6561](https://github.com/George6561)
