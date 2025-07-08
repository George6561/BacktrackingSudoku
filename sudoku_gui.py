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

import tkinter as tk
from PIL import Image, ImageTk
import ctypes
from ctypes import wintypes
from sudoku_board import SudokuBoard


class SudokuApp:
    def __init__(self, root):
        """
        Initializes the Sudoku GUI application.

        This sets up the main window, loads graphical assets, draws the Sudoku board,
        binds user input (keyboard and mouse), and initializes the puzzle grid.

        Args:
            root (tk.Tk): The root tkinter window.

        Key responsibilities:
            - Create a SudokuBoard logic backend.
            - Load and render the board background image.
            - Create and position Solve and Clear buttons.
            - Highlight and track the selected cell.
            - Bind keyboard input for navigation and value entry.
            - Load and display the initial puzzle board.
        """
        self.root = root
        self.root.title("Sudoku Solver")

        # Create SudokuBoard instance
        self.board = SudokuBoard()
        self.selected_cell = None  # (row, col)

        # Load the board image
        board_image_path = "SudokuBoard.jpg"
        self.board_image = Image.open(board_image_path)
        self.board_photo = ImageTk.PhotoImage(self.board_image)

        self.board_width, self.board_height = self.board_image.size
        total_height = 646 + 34
        self.root.geometry(f"{self.board_width}x{total_height}")
        self.root.resizable(False, False)
        self.center_window(self.board_width, total_height)

        self.canvas = tk.Canvas(self.root, width=self.board_width, height=total_height, highlightthickness=0)
        self.canvas.pack()

        # Draw the board background
        self.canvas.create_image(0, 0, anchor="nw", image=self.board_photo)

        # Click listener for cells
        self.canvas.bind("<Button-1>", self.on_board_click)

        # Rectangle highlight overlay (hidden initially)
        self.highlight_rect = self.canvas.create_rectangle(0, 0, 0, 0, fill="yellow", outline="", state='hidden')

        # Load and place buttons (same as before)
        self.solve_imgs = [ImageTk.PhotoImage(Image.open(f"Solve{i}.png")) for i in range(3)]
        self.clear_imgs = [ImageTk.PhotoImage(Image.open(f"Clear{i}.png")) for i in range(3)]
        btn_y, solve_x, clear_x = 646, 37, 547

        self.solve_button = self.canvas.create_image(solve_x, btn_y, anchor="nw", image=self.solve_imgs[0])
        self.canvas.tag_bind(self.solve_button, "<Enter>",
                             lambda e: self.canvas.itemconfig(self.solve_button, image=self.solve_imgs[1]))
        self.canvas.tag_bind(self.solve_button, "<Leave>",
                             lambda e: self.canvas.itemconfig(self.solve_button, image=self.solve_imgs[0]))
        self.canvas.tag_bind(self.solve_button, "<ButtonPress-1>",
                             lambda e: self.canvas.itemconfig(self.solve_button, image=self.solve_imgs[2]))
        self.canvas.tag_bind(self.solve_button, "<ButtonRelease-1>", self.on_solve)

        self.clear_button = self.canvas.create_image(clear_x, btn_y, anchor="nw", image=self.clear_imgs[0])
        self.canvas.tag_bind(self.clear_button, "<Enter>",
                             lambda e: self.canvas.itemconfig(self.clear_button, image=self.clear_imgs[1]))
        self.canvas.tag_bind(self.clear_button, "<Leave>",
                             lambda e: self.canvas.itemconfig(self.clear_button, image=self.clear_imgs[0]))
        self.canvas.tag_bind(self.clear_button, "<ButtonPress-1>",
                             lambda e: self.canvas.itemconfig(self.clear_button, image=self.clear_imgs[2]))
        self.canvas.tag_bind(self.clear_button, "<ButtonRelease-1>", self.on_clear)

        # Start with top-left cell selected
        self.selected_index = 0
        self.selected_cell = (0, 0)
        self.highlight_selected_cell()

        # Arrow key bindings
        self.root.bind("<Left>", lambda e: self.move_selection(-1))
        self.root.bind("<Right>", lambda e: self.move_selection(1))
        self.root.bind("<Up>", lambda e: self.move_selection(-9))
        self.root.bind("<Down>", lambda e: self.move_selection(9))

        # Number key input
        self.root.bind("<Key>", self.on_key_press)

        # Load number images 1–9
        self.number_images = {
            i: ImageTk.PhotoImage(Image.open(f"{i}.png")) for i in range(1, 10)
        }

        # Track canvas image IDs in a grid for redrawing/clearing
        self.number_ids = [[None for _ in range(9)] for _ in range(9)]

        # Initial board values
        initial_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

        # Load into the board
        for row in range(9):
            for col in range(9):
                self.board.set_value(row, col, initial_board[row][col])

        # Draw the numbers
        self.redraw_board()

    def move_selection(self, delta):
        new_index = self.selected_index + delta
        if 0 <= new_index < 81:
            new_row = new_index // 9
            new_col = new_index % 9
            self.selected_index = new_index
            self.selected_cell = (new_row, new_col)
            self.highlight_selected_cell()

    def highlight_selected_cell(self):
        row, col = self.selected_cell
        x1, y1, x2, y2 = self.cell_bounds(row, col)
        self.canvas.coords(self.highlight_rect, x1 + 1, y1 + 1, x2 - 1, y2 - 1)
        self.canvas.itemconfig(self.highlight_rect, state='normal')

    def on_board_click(self, event):
        x, y = event.x, event.y
        cell = self.pixel_to_cell(x, y)
        if cell:
            row, col = cell
            self.selected_cell = (row, col)
            self.selected_index = row * 9 + col

            print(f"Clicked cell: ({row}, {col})")

            # Update highlight rectangle
            x1, y1, x2, y2 = self.cell_bounds(row, col)
            self.canvas.coords(self.highlight_rect, x1 + 1, y1 + 1, x2 - 2, y2 - 2)
            self.canvas.itemconfig(self.highlight_rect, state='normal')
        else:
            self.canvas.itemconfig(self.highlight_rect, state='hidden')

    def pixel_to_cell(self, x, y):
        origin_x, origin_y = 37, 19
        cell_size = 66
        short_gap = 2
        block_gap = 8

        for row in range(9):
            for col in range(9):
                x1, y1, x2, y2 = self.cell_bounds(row, col)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return row, col
        return None

    def cell_bounds(self, row, col):
        origin_x, origin_y = 37, 19
        cell_size = 66
        short_gap = 2
        block_gap = 8

        # Total horizontal gap before this column
        gap_x = (col * short_gap) + (col // 3) * (block_gap - short_gap)
        gap_y = (row * short_gap) + (row // 3) * (block_gap - short_gap)

        x1 = origin_x + col * cell_size + gap_x
        y1 = origin_y + row * cell_size + gap_y
        x2 = x1 + cell_size
        y2 = y1 + cell_size

        return x1, y1, x2, y2

    def on_solve(self, event):
        self.canvas.itemconfig(self.solve_button, image=self.solve_imgs[1])
        if self.board.solve():
            print("Board solved!")
            self.redraw_board()
        else:
            print("No solution exists.")

    def on_clear(self, event):
        self.canvas.itemconfig(self.clear_button, image=self.clear_imgs[1])
        self.board.clear()
        self.canvas.itemconfig(self.highlight_rect, state='hidden')
        self.redraw_board()
        print("Board cleared.")

    def redraw_board(self):
        for row in range(9):
            for col in range(9):
                self.draw_number(row, col)

    def center_window(self, width, height):
        user32 = ctypes.windll.user32
        work_area = wintypes.RECT()
        ctypes.windll.user32.SystemParametersInfoW(0x0030, 0, ctypes.byref(work_area), 0)

        work_width = work_area.right - work_area.left
        work_height = work_area.bottom - work_area.top

        x = int((work_width / 2) - (width / 2))
        y = int((work_height / 2) - (height / 2))

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def on_key_press(self, event):
        if self.selected_cell is None:
            return

        row, col = self.selected_cell

        # Accept digits 1-9
        if event.char in "123456789":
            value = int(event.char)
            if self.board.set_value(row, col, value):
                self.draw_number(row, col)
                print(f"Set cell ({row}, {col}) to {value}")
            else:
                print(f"Invalid value {value} for cell ({row}, {col})")

        # Clear on 0, backspace, or delete
        elif event.char == "0" or event.keysym in ("BackSpace", "Delete"):
            self.board.set_value(row, col, 0)
            print(f"Cleared cell ({row}, {col})")

    def draw_number(self, row, col):
        # Clear any existing image
        if self.number_ids[row][col]:
            self.canvas.delete(self.number_ids[row][col])
            self.number_ids[row][col] = None

        value = self.board.get_value(row, col)
        if 1 <= value <= 9:
            x1, y1, x2, y2 = self.cell_bounds(row, col)
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            image_id = self.canvas.create_image(center_x, center_y, image=self.number_images[value])
            self.number_ids[row][col] = image_id
