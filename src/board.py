import tkinter as tk
from tkinter import ttk
from piece import Piece


class Board:
    def __init__(self, root):
        self.root = root
        self.board_size = 8
        self.squares = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.selected_piece = None
        self.move_history = []
        self.setup_pieces()

        self.input_var = tk.StringVar()  # To handle move input
        self.setup_ui()

    def setup_pieces(self):
        """Initialize the chessboard with binary pieces in the correct positions."""
        # Set up white pieces
        for col in range(self.board_size):
            self.squares[1][col] = Piece('Pawn', 'white')  # White pawns
        self.squares[0][0] = self.squares[0][7] = Piece('Rook', 'white')  # White rooks
        self.squares[0][1] = self.squares[0][6] = Piece('Knight', 'white')  # White knights
        self.squares[0][2] = self.squares[0][5] = Piece('Bishop', 'white')  # White bishops
        self.squares[0][3] = Piece('Queen', 'white')  # White queen
        self.squares[0][4] = Piece('King', 'white')  # White king

        # Set up black pieces
        for col in range(self.board_size):
            self.squares[6][col] = Piece('Pawn', 'black')  # Black pawns
        self.squares[7][0] = self.squares[7][7] = Piece('Rook', 'black')  # Black rooks
        self.squares[7][1] = self.squares[7][6] = Piece('Knight', 'black')  # Black knights
        self.squares[7][2] = self.squares[7][5] = Piece('Bishop', 'black')  # Black bishops
        self.squares[7][3] = Piece('Queen', 'black')  # Black queen
        self.squares[7][4] = Piece('King', 'black')  # Black king

    def setup_ui(self):
        """Set up the user interface with the board and input row."""
        self.root.configure(bg="#3b3b3b")  # Dark background
        self.create_frames()  # Organize layout into frames
        self.draw_labels()
        self.draw_board()
        self.draw_input_area()
        self.draw_move_history()

    def create_frames(self):
        """Create frames to better organize the layout."""
        self.board_frame = tk.Frame(self.root, bg="#3b3b3b")
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        self.input_frame = tk.Frame(self.root, bg="#3b3b3b")
        self.input_frame.grid(row=1, column=0, padx=10, pady=10)

        self.history_frame = tk.Frame(self.root, bg="#3b3b3b")
        self.history_frame.grid(row=2, column=0, padx=10, pady=10)

    def draw_labels(self):
        """Draw the row and column labels with reversed rows and alphabet order."""
        # Labels for columns ('a' to 'h' on bottom, 'a' to 'h' on top)
        for col in range(1, self.board_size + 1):
            # Bottom labels: 'a' to 'h'
            tk.Label(self.board_frame, text=chr(96 + col), font=("Courier", 14, "bold"),
                     width=3, height=1, bg="#2b2b2b", fg="white").grid(row=self.board_size + 1, column=col, padx=2, pady=2)

            # Top labels: 'a' to 'h' (reversed from previous)
            tk.Label(self.board_frame, text=chr(96 + col), font=("Courier", 14, "bold"),
                     width=3, height=1, bg="#2b2b2b", fg="white").grid(row=0, column=col, padx=2, pady=2)

        # Labels for rows ('8' to '1' on both sides)
        for row in range(1, self.board_size + 1):
            # Left side: '8' to '1'
            tk.Label(self.board_frame, text=str(self.board_size + 1 - row), font=("Courier", 14, "bold"),
                     width=2, height=1, bg="#2b2b2b", fg="white").grid(row=row, column=0, padx=2, pady=2)

            # Right side: '8' to '1'
            tk.Label(self.board_frame, text=str(self.board_size + 1 - row), font=("Courier", 14, "bold"),
                     width=2, height=1, bg="#2b2b2b", fg="white").grid(row=row, column=self.board_size + 1, padx=2, pady=2)

    def draw_board(self):
        """Draw the 8x8 board with binary values and modern design."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                piece = self.squares[row][col]
                binary_value = piece.get_binary_value() if piece else "----"

                bg_color = "#1f1f1f" if (row + col) % 2 == 0 else "#3d3d3d"  # Chessboard colors
                label = tk.Label(
                    self.board_frame, text=binary_value, font=("Courier", 16),
                    width=5, height=2, bg=bg_color, fg="white", relief=tk.RIDGE
                )
                label.grid(row=row + 1, column=col + 1, padx=1, pady=1)

    def draw_input_area(self):
        """Create an input area at the bottom with enhanced styling."""
        input_label = tk.Label(self.input_frame, text="Move (e.g., e2 to e4):", font=("Courier", 14), fg="white",
                               bg="#3b3b3b")
        input_label.grid(row=0, column=0, sticky="w")

        input_entry = tk.Entry(self.input_frame, textvariable=self.input_var, font=("Courier", 14), width=30,
                               bg="#252525", fg="white", insertbackground="white")
        input_entry.grid(row=0, column=1, sticky="e", padx=10)
        input_entry.bind("<Return>", self.handle_move_input)

    def draw_move_history(self):
        """Create a styled move history area with a scrollbar."""
        history_label = tk.Label(self.history_frame, text=" Move History:", font=("Courier", 14), fg="white",
                                 bg="#3b3b3b")
        history_label.grid(row=0, column=0, sticky="w")

        self.history_display = tk.Text(self.history_frame, height=4, width=62, font=("Courier", 12), bg="#252525",
                                       fg="lightgreen", wrap="word", state=tk.DISABLED)
        self.history_display.grid(row=1, column=0, sticky="we", padx=10, pady=5)

        scroll = ttk.Scrollbar(self.history_frame, command=self.history_display.yview)
        self.history_display.config(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=1, sticky="ns")

    def handle_move_input(self, event):
        """Handle the player's move input."""
        move = self.input_var.get().strip()  # Get the move from the input field
        self.input_var.set("")  # Clear the input field

        if self.is_valid_move_format(move):
            self.move_history.append(move)
            self.update_move_history_display()

    def update_move_history_display(self):
        """Update the move history display with the latest move."""
        self.history_display.config(state=tk.NORMAL)
        self.history_display.delete(1.0, tk.END)  # Clear current history
        for move in self.move_history:
            self.history_display.insert(tk.END, f"{move}, ")  # Add each move
        self.history_display.config(state=tk.DISABLED)

    def is_valid_move_format(self, move):
        """Check if the input is in a valid move format (e.g., 'e2 to e4')."""
        if len(move) == 8 and move[0] in "abcdefgh" and move[1] in "12345678" and move[2:6] == " to " and move[
            6] in "abcdefgh" and move[7] in "12345678":
            return True
        return False
