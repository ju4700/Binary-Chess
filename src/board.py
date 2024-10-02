import os
import pickle
import tkinter as tk
from tkinter import messagebox, simpledialog
from piece import Piece

class Board:
    def __init__(self, root):
        self.root = root
        self.board_size = 8
        self.squares = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.selected_piece = None
        self.selected_square = None
        self.move_history = []
        self.current_turn = 'white'  
        self.setup_pieces()
        self.setup_ui()
        self.create_menu()

    def create_menu(self):
        """Create a futuristic styled menu bar for the application."""
        menubar = tk.Menu(self.root, bg="#1f1f1f", fg="#c8e8e6", activebackground="#2b2b2b", activeforeground="white")

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0, bg="#1f1f1f", fg="white", activebackground="#2b2b2b",
                            activeforeground="#c8e8e6")
        file_menu.add_command(label="New Game", command=self.new_game, font=("Consolas", 12))
        file_menu.add_command(label="Save Game", command=self.save_game, font=("Consolas", 12))
        file_menu.add_command(label="Load Game", command=self.load_game, font=("Consolas", 12))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, font=("Consolas", 12))

        menubar.add_cascade(label="File", menu=file_menu, font=("Consolas", 12, "bold"))

        def on_enter(event):
            event.widget.config(bg="#3d3d3d", fg="#00FF00")

        def on_leave(event):
            event.widget.config(bg="#1f1f1f", fg="white")

        for item in file_menu.winfo_children():
            item.bind("<Enter>", on_enter)
            item.bind("<Leave>", on_leave)

        self.root.config(menu=menubar) 

    def new_game(self):
        """Start a new game."""
        self.move_history.clear()
        self.current_turn = 'white'
        self.setup_pieces()
        self.draw_board() 

    def save_game(self):
        """Save the current game state."""
        filename = simpledialog.askstring("Save Game", "Enter a name for the saved game:")
        if filename:
            save_path = os.path.join("Saved games", f"{filename}.pkl")
            os.makedirs("Saved games", exist_ok=True)  

            with open(save_path, "wb") as f:
                game_state = {
                    "squares": self.squares,
                    "move_history": self.move_history,
                    "current_turn": self.current_turn,
                }
                pickle.dump(game_state, f)
                messagebox.showinfo("Save Game", "Game saved successfully!")

    def load_game(self):
        """Load a game state."""
        filename = simpledialog.askstring("Load Game", "Enter the name of the saved game:")
        if filename:
            load_path = os.path.join("Saved games", f"{filename}.pkl")
            if os.path.exists(load_path):
                with open(load_path, "rb") as f:
                    game_state = pickle.load(f)
                    self.squares = game_state["squares"]
                    self.move_history = game_state["move_history"]
                    self.current_turn = game_state["current_turn"]
                    self.draw_board() 
                    self.update_move_history_display()  
                    self.update_status_display() 
                    messagebox.showinfo("Load Game", "Game loaded successfully!")
            else:
                messagebox.showerror("Load Game", "Game not found!")

    def setup_pieces(self):
        """Initialize the chessboard with pieces in the correct positions."""
        for col in range(self.board_size):
            self.squares[1][col] = Piece('Pawn', 'white')  # White pawns
        self.squares[0][0] = self.squares[0][7] = Piece('Rook', 'white')  # White rooks
        self.squares[0][1] = self.squares[0][6] = Piece('Knight', 'white')  # White knights
        self.squares[0][2] = self.squares[0][5] = Piece('Bishop', 'white')  # White bishops
        self.squares[0][3] = Piece('Queen', 'white')  # White queen
        self.squares[0][4] = Piece('King', 'white')  # White king

        for col in range(self.board_size):
            self.squares[6][col] = Piece('Pawn', 'black')  # Black pawns
        self.squares[7][0] = self.squares[7][7] = Piece('Rook', 'black')  # Black rooks
        self.squares[7][1] = self.squares[7][6] = Piece('Knight', 'black')  # Black knights
        self.squares[7][2] = self.squares[7][5] = Piece('Bishop', 'black')  # Black bishops
        self.squares[7][3] = Piece('Queen', 'black')  # Black queen
        self.squares[7][4] = Piece('King', 'black')  # Black king

    def setup_ui(self):
        """Set up the user interface with the board and input row."""
        self.root.configure(bg="#3b3b3b")  
        self.create_frames()  
        self.draw_labels()
        self.draw_board()
        self.draw_move_history()
        self.draw_status_box() 

    def create_frames(self):
        """Create frames to better organize the layout."""
        self.board_frame = tk.Frame(self.root, bg="#3b3b3b")
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        self.history_frame = tk.Frame(self.root, bg="#3b3b3b")
        self.history_frame.grid(row=2, column=0, padx=10, pady=10)

        self.status_frame = tk.Frame(self.root, bg="#3b3b3b") 
        self.status_frame.grid(row=1, column=0, padx=10, pady=10)

    def draw_labels(self):
        """Draw the row and column labels."""
        for col in range(1, self.board_size + 1):
            tk.Label(self.board_frame, text=chr(96 + col), font=("Courier", 14, "bold"),
                     width=3, height=1, bg="#2b2b2b", fg="white").grid(row=self.board_size + 1, column=col, padx=2,
                                                                       pady=2)

            tk.Label(self.board_frame, text=chr(96 + col), font=("Courier", 14, "bold"),
                     width=3, height=1, bg="#2b2b2b", fg="white").grid(row=0, column=col, padx=2, pady=2)

        for row in range(1, self.board_size + 1):
            tk.Label(self.board_frame, text=str(self.board_size + 1 - row), font=("Courier", 14, "bold"),
                     width=2, height=1, bg="#2b2b2b", fg="white").grid(row=row, column=0, padx=2, pady=2)

            tk.Label(self.board_frame, text=str(self.board_size + 1 - row), font=("Courier", 14, "bold"),
                     width=2, height=1, bg="#2b2b2b", fg="white").grid(row=row, column=self.board_size + 1, padx=2,
                                                                       pady=2)

    def draw_board(self):
        """Draw the 8x8 board with pieces."""
        for row in range(self.board_size):
            for col in range(self.board_size):
                self.draw_square(row, col)

    def draw_square(self, row, col):
        """Redraw a specific square on the board."""
        piece = self.squares[row][col]
        binary_value = piece.get_binary_value() if piece else "----"

        bg_color = "#1f1f1f" if (row + col) % 2 == 0 else "#3d3d3d"  # Chessboard colors
        label = tk.Label(
            self.board_frame, text=binary_value, font=("Courier", 16),
            width=5, height=2, bg=bg_color, fg="white", relief=tk.RIDGE
        )
        label.grid(row=row + 1, column=col + 1, padx=1, pady=1)
        label.bind("<Button-1>", lambda e, r=row, c=col: self.select_square(r, c)) 

    def select_square(self, row, col):
        """Select a square or move a selected piece."""
        if self.selected_square:
            self.make_move(self.selected_square, (row, col))
            self.selected_square = None
        elif self.squares[row][col] and self.squares[row][col].color == self.current_turn:
            self.selected_square = (row, col)

    def make_move(self, from_square, to_square):
        """Move a piece from one square to another."""
        from_row, from_col = from_square
        to_row, to_col = to_square

        piece = self.squares[from_row][from_col]
        if piece and piece.is_valid_move(from_square, to_square, self.squares):
            target_piece = self.squares[to_row][to_col]
            self.squares[to_row][to_col] = piece
            self.squares[from_row][from_col] = None
            self.move_history.append(f"{self.index_to_square(from_square)} to {self.index_to_square(to_square)}")
            self.update_move_history_display()

            self.update_square(from_row, from_col) 
            self.update_square(to_row, to_col) 
            if piece.piece_type == 'King':
                if piece.is_in_check((to_row, to_col), self.squares):
                    self.display_status("Check!")
                if piece.is_checkmate((to_row, to_col), self.squares):
                    self.display_status("Checkmate!")
                    return

            self.current_turn = 'black' if self.current_turn == 'white' else 'white'
            self.update_status_display()

        else:
            self.display_status("Invalid Move!", duration=2000) 

    def update_square(self, row, col):
        """Update the display of a specific square on the board."""
        piece = self.squares[row][col]
        binary_value = piece.get_binary_value() if piece else "----"
        bg_color = "#1f1f1f" if (row + col) % 2 == 0 else "#3d3d3d" 

        square_label = self.board_frame.grid_slaves(row=row + 1, column=col + 1)[0]
        square_label.config(text=binary_value, bg=bg_color)

    def index_to_square(self, index):
        """Convert board indices to chess notation (e.g., (6, 4) -> 'e2')."""
        row, col = index
        return f"{chr(col + 97)}{self.board_size - row}"

    def draw_move_history(self):
        """Create a move history area."""
        history_label = tk.Label(self.history_frame, text=" Move History:", font=("Courier", 14), fg="white",
                                 bg="#3b3b3b")
        history_label.grid(row=0, column=0, sticky="w")

        self.history_display = tk.Text(self.history_frame, height=4, width=62, font=("Consolas", 12), bg="#252525",
                                       fg="white", wrap="word", state=tk.DISABLED)
        self.history_display.grid(row=1, column=0, sticky="we", padx=10, pady=5)

        scroll = tk.Scrollbar(self.history_frame, command=self.history_display.yview)
        self.history_display.config(yscrollcommand=scroll.set)
        scroll.grid(row=1, column=1, sticky="ns")

    def update_move_history_display(self):
        """Update the move history display with the latest move."""
        self.history_display.config(state=tk.NORMAL)
        self.history_display.delete(1.0, tk.END) 
        self.history_display.insert(tk.END, " ")
        for move in self.move_history:
            self.history_display.insert(tk.END, f"{move}, ")
        self.history_display.config(state=tk.DISABLED) 

    def update_status_display(self):
        """Update the status display with the current turn."""
        self.status_display.config(text=f"Current Turn: {self.current_turn.capitalize()}")

    def display_status(self, message, duration=None):
        """Display a status message."""
        self.status_display.config(text=message)
        if duration:
            self.root.after(duration, lambda: self.status_display.config(text=f"Current Turn: {self.current_turn.capitalize()}"))

    def draw_status_box(self):
        """Draw the status box for current turn."""
        self.status_display = tk.Label(self.status_frame, text=f"Current Turn: {self.current_turn.capitalize()}",
                                       font=("Courier", 14), bg="#3b3b3b", fg="white")
        self.status_display.pack()
