"""
Copyright (c) 2024
George Miller

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

class SudokuBoard:
    def __init__(self):
        # Initialize a 9x9 board filled with zeros
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def set_value(self, row, col, value):
        """Sets a value on the board if it's legal."""
        if 0 <= value <= 9 and 0 <= row < 9 and 0 <= col < 9:
            if value == 0 or self.is_valid(row, col, value):
                self.board[row][col] = value
                return True
        return False

    def get_value(self, row, col):
        """Returns the value at the given cell."""
        if 0 <= row < 9 and 0 <= col < 9:
            return self.board[row][col]
        return None

    def is_valid(self, row, col, value):
        """Checks if placing the value at (row, col) is valid."""

        # Check row
        for c in range(9):
            if self.board[row][c] == value and c != col:
                return False

        # Check column
        for r in range(9):
            if self.board[r][col] == value and r != row:
                return False

        # Check 3x3 box
        box_start_row = row - row % 3
        box_start_col = col - col % 3
        for r in range(box_start_row, box_start_row + 3):
            for c in range(box_start_col, box_start_col + 3):
                if self.board[r][c] == value and (r, c) != (row, col):
                    return False

        return True

    def find_empty(self):
        """Finds an empty cell (returns tuple) or None if full."""
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def solve(self):
        """Solves the board using backtracking."""
        empty = self.find_empty()
        if not empty:
            return True  # Solved

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = 0  # backtrack

        return False  # Trigger backtracking

    def clear(self):
        """Resets the entire board."""
        self.board = [[0 for _ in range(9)] for _ in range(9)]

    def __str__(self):
        """Pretty-print the board (for console/debug use)."""
        result = ""
        for i, row in enumerate(self.board):
            result += " ".join(str(val) if val != 0 else "." for val in row)
            result += "\n"
        return result
