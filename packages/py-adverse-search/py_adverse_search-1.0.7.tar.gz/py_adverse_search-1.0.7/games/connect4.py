class Connect4:
    ROWS = 6
    COLS = 7
    EMPTY = ' '

    def __init__(self):
        self.board = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.HUMAN = None
        self.COMP = None

    def clean(self):
        """
        Resets the board to the initial empty state.
        """
        self.board = [[self.EMPTY for _ in range(self.COLS)] for _ in range(self.ROWS)]

    def render(self):
        """
        Renders the current state of the board.
        """
        for row in self.board:
            print("|" + "|".join(row) + "|")
        print(" " + " ".join(map(str, range(self.COLS))))

    def drop_piece(self, col, piece):
        """
        Drops a piece into the specified column.
        
        :param col: The column to drop the piece into.
        :param piece: The piece to drop (HUMAN or COMP).
        :return: True if the piece was successfully dropped, False otherwise.
        """
        for row in reversed(self.board):
            if row[col] == self.EMPTY:
                row[col] = piece
                return True
        return False

    def empty_cells(self):
        """
        Checks if there are any empty cells left on the board.
        
        :return: True if there are empty cells, False otherwise.
        """
        return any(self.EMPTY in row for row in self.board)

    def valid_moves(self):
        """
        Gets a list of valid columns where a piece can be dropped.
        
        :return: A list of column indices that are valid moves.
        """
        return [col for col in range(self.COLS) if self.board[0][col] == self.EMPTY]

    def wins(self, piece):
        """
        Checks if the specified piece has won the game.
        
        :param piece: The piece to check (HUMAN or COMP).
        :return: True if the specified piece has won, False otherwise.
        """
        # Check horizontal locations for win
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row][col + i] == piece for i in range(4)):
                    return True
        # Check vertical locations for win
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if all(self.board[row + i][col] == piece for i in range(4)):
                    return True
        # Check positively sloped diagonals
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(self.board[row + i][col + j] == piece for i, j in zip(range(4), range(4))):
                    return True
                if all(self.board[row + i][col + j] == piece for i, j in zip(range(4), range(-4, 0))):
                    return True
        return False

    def game_over(self):
        """
        Checks if the game is over (either player has won or the board is full).
        
        :return: True if the game is over, False otherwise.
        """
        return self.wins(self.HUMAN) or self.wins(self.COMP) or not self.empty_cells()

    def human_turn(self, piece):
        """
        Handles the human player's turn.
        
        :param piece: The piece to drop (HUMAN).
        """
        valid = False
        while not valid:
            col = input(f"Choose a column (0-{self.COLS - 1}): ")
            try:
                col = int(col)
                if col in self.valid_moves():
                    self.drop_piece(col, piece)
                    valid = True
                else:
                    print("Column full! Try again.")
            except ValueError:
                print("Invalid input! Try again.")

    def copy(self):
        """
        Creates a deep copy of the board.
        
        :return: A new Connect4 instance with the same board state.
        """
        new_board = Connect4()
        new_board.board = [row[:] for row in self.board]
        new_board.HUMAN = self.HUMAN
        new_board.COMP = self.COMP
        return new_board
