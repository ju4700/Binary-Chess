class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color

    def get_binary_value(self):
        """Get binary representation based on piece type and color."""
        binary_map = {
            'Pawn': '0001' if self.color == 'white' else '1001',
            'Rook': '0010' if self.color == 'white' else '1010',
            'Knight': '0011' if self.color == 'white' else '1011',
            'Bishop': '0100' if self.color == 'white' else '1100',
            'Queen': '0101' if self.color == 'white' else '1101',
            'King': '0110' if self.color == 'white' else '1110',
        }
        return binary_map[self.piece_type]

    def is_valid_move(self, from_square, to_square, squares):
        """Check if the move is valid for the piece."""
        from_row, from_col = from_square
        to_row, to_col = to_square

        # Check boundaries
        if not (0 <= to_row < 8 and 0 <= to_col < 8):
            return False

        if self.piece_type == 'Pawn':
            return self.is_valid_pawn_move(from_row, from_col, to_row, to_col, squares)
        elif self.piece_type == 'Rook':
            return self.is_valid_rook_move(from_row, from_col, to_row, to_col, squares)
        elif self.piece_type == 'Knight':
            return self.is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif self.piece_type == 'Bishop':
            return self.is_valid_bishop_move(from_row, from_col, to_row, to_col, squares)
        elif self.piece_type == 'Queen':
            return self.is_valid_queen_move(from_row, from_col, to_row, to_col, squares)
        elif self.piece_type == 'King':
            return self.is_valid_king_move(from_row, from_col, to_row, to_col)
        return False

    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col, squares):
        """Validate pawn movement."""
        direction = 1 if self.color == 'white' else -1
        start_row = 1 if self.color == 'white' else 6

        # Move forward
        if (to_col == from_col) and (to_row == from_row + direction) and (squares[to_row][to_col] is None):
            return True
        # Double move from starting position
        elif (to_col == from_col) and (to_row == from_row + 2 * direction) and (
                from_row == start_row and squares[to_row][to_col] is None and squares[from_row + direction][
            to_col] is None):
            return True
        # Capture move
        elif (abs(to_col - from_col) == 1) and (to_row == from_row + direction) and (
                squares[to_row][to_col] is not None and squares[to_row][to_col].color != self.color):
            return True
        return False

    def is_valid_rook_move(self, from_row, from_col, to_row, to_col, squares):
        """Validate rook movement."""
        if from_row == to_row:  # Horizontal movement
            step = 1 if to_col > from_col else -1
            for col in range(from_col + step, to_col, step):
                if squares[from_row][col] is not None:
                    return False
            return True
        elif from_col == to_col:  # Vertical movement
            step = 1 if to_row > from_row else -1
            for row in range(from_row + step, to_row, step):
                if squares[row][from_col] is not None:
                    return False
            return True
        return False

    def is_valid_knight_move(self, from_row, from_col, to_row, to_col):
        """Validate knight movement."""
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

    def is_valid_bishop_move(self, from_row, from_col, to_row, to_col, squares):
        """Validate bishop movement."""
        if abs(to_row - from_row) == abs(to_col - from_col):  # Diagonal movement
            row_step = 1 if to_row > from_row else -1
            col_step = 1 if to_col > from_col else -1
            row, col = from_row + row_step, from_col + col_step
            while (row != to_row) and (col != to_col):
                if squares[row][col] is not None:
                    return False
                row += row_step
                col += col_step
            return True
        return False

    def is_valid_queen_move(self, from_row, from_col, to_row, to_col, squares):
        """Validate queen movement (combines rook and bishop)."""
        return self.is_valid_rook_move(from_row, from_col, to_row, to_col, squares) or \
               self.is_valid_bishop_move(from_row, from_col, to_row, to_col, squares)

    def is_valid_king_move(self, from_row, from_col, to_row, to_col):
        """Validate king movement."""
        return max(abs(to_row - from_row), abs(to_col - from_col)) == 1

    def is_in_check(self, king_position, squares):
        """Check if the king is in check."""
        for row in range(len(squares)):
            for col in range(len(squares[row])):
                piece = squares[row][col]
                if piece and piece.color != self.color:  # Check opposing pieces
                    if piece.is_valid_move((row, col), king_position, squares):
                        return True
        return False

    def is_checkmate(self, king_position, squares):
        """Determine if the king is in checkmate."""
        if not self.is_in_check(king_position, squares):
            return False

        # Try all possible moves for the king to see if it can escape
        king_row, king_col = king_position
        for row in range(max(0, king_row - 1), min(8, king_row + 2)):
            for col in range(max(0, king_col - 1), min(8, king_col + 2)):
                if (row, col) != king_position and (0 <= row < 8 and 0 <= col < 8):
                    # Temporarily move the king to see if it can escape
                    original_piece = squares[row][col]
                    squares[row][col] = Piece('King', self.color)  # Simulate king move
                    if not self.is_in_check(king_position, squares):
                        squares[row][col] = original_piece  # Restore piece
                        return False  # King can escape
                    squares[row][col] = original_piece  # Restore piece
        return True  # No escape found

    def __repr__(self):
        """Return a string representation for easier debugging."""
        return f"{self.color} {self.piece_type}"
