import tkinter as tk
from board import Board


class BinaryChessGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Binary Chess")
        self.board = Board(self.root)

    def run(self):
        self.board.draw_board()  # Draw the initial binary board
        self.root.mainloop()
