class Piece:
    PIECE_VALUES = {
        'Pawn': '0001',
        'Rook': '0010',
        'Knight': '0011',
        'Bishop': '0100',
        'Queen': '0101',
        'King': '0110'
    }

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.binary_value = self.PIECE_VALUES.get(name, "----")

    def get_binary_value(self):
        """Return the binary value of the piece."""
        return self.binary_value
