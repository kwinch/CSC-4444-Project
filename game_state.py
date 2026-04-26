from copy import deepcopy


class Connect43D:
    """
    Board layout:
        board[z][y][x]

    Coordinates:
        x = column
        y = row
        z = height

    Pieces fall to the lowest available z in a chosen (x, y) stack.
    """

    def __init__(self, height=6, rows=6, cols=7, connect_n=4):
        self.height = height
        self.rows = rows
        self.cols = cols
        self.connect_n = connect_n

        self.board = None
        self.current_player = 1
        self.winner = 0
        self.last_move = None

        self.reset()

    def reset(self):
        self.board = [
            [
                [0 for _ in range(self.cols)]
                for _ in range(self.rows)
            ]
            for _ in range(self.height)
        ]
        self.current_player = 1
        self.winner = 0
        self.last_move = None

    def clone(self):
        new_game = Connect43D(self.height, self.rows, self.cols, self.connect_n)
        new_game.board = deepcopy(self.board)
        new_game.current_player = self.current_player
        new_game.winner = self.winner
        new_game.last_move = self.last_move
        return new_game

    def in_bounds(self, x, y, z=None):
        if z is None:
            return 0 <= x < self.cols and 0 <= y < self.rows
        return 0 <= x < self.cols and 0 <= y < self.rows and 0 <= z < self.height

    def is_valid_move(self, x, y):
        if not self.in_bounds(x, y):
            return False
        return self.board[self.height - 1][y][x] == 0

    def get_available_z(self, x, y):
        if not self.is_valid_move(x, y):
            return None

        for z in range(self.height):
            if self.board[z][y][x] == 0:
                return z

        return None

    def get_legal_moves(self):
        moves = []
        for y in range(self.rows):
            for x in range(self.cols):
                if self.is_valid_move(x, y):
                    moves.append((x, y))
        return moves

    def make_move(self, x, y, player=None):
        """
        Place a piece in column x, row y.

        Returns:
            z coordinate where the piece landed.

        Raises:
            ValueError if the move is invalid or the game is already over.
        """
        if self.winner != 0:
            raise ValueError("Game is already over.")

        if player is None:
            player = self.current_player

        if player not in (1, 2):
            raise ValueError("Player must be 1 or 2.")

        z = self.get_available_z(x, y)
        if z is None:
            raise ValueError(f"Invalid move at ({x}, {y}).")

        self.board[z][y][x] = player
        self.last_move = (x, y, z, player)

        if self.check_win_from_position(x, y, z, player):
            self.winner = player
        elif self.is_full():
            self.winner = -1
        else:
            self.current_player = 2 if self.current_player == 1 else 1

        return z

    def undo_move(self):
        """
        Remove the most recent move.
        Useful later if your team adds minimax or move search.
        """
        if self.last_move is None:
            raise ValueError("No moves to undo.")

        x, y, z, player = self.last_move
        self.board[z][y][x] = 0
        self.current_player = player
        self.winner = 0
        self.last_move = None

    def is_full(self):
        return len(self.get_legal_moves()) == 0

    def check_win_from_position(self, x, y, z, player):
        """
        Check all 3D line directions through (x, y, z).
        There are 13 unique directions if opposite directions are counted together.
        """
        directions = [
            (1, 0, 0),   (0, 1, 0),   (0, 0, 1),
            (1, 1, 0),   (1, -1, 0),
            (1, 0, 1),   (1, 0, -1),
            (0, 1, 1),   (0, 1, -1),
            (1, 1, 1),   (1, 1, -1),
            (1, -1, 1),  (1, -1, -1),
        ]

        for dx, dy, dz in directions:
            count = 1
            count += self._count_direction(x, y, z, dx, dy, dz, player)
            count += self._count_direction(x, y, z, -dx, -dy, -dz, player)
            if count >= self.connect_n:
                return True

        return False

    def _count_direction(self, x, y, z, dx, dy, dz, player):
        count = 0
        cx, cy, cz = x + dx, y + dy, z + dz

        while self.in_bounds(cx, cy, cz) and self.board[cz][cy][cx] == player:
            count += 1
            cx += dx
            cy += dy
            cz += dz

        return count

    def get_winner(self):
        return self.winner

    def get_cell(self, x, y, z):
        if not self.in_bounds(x, y, z):
            raise ValueError("Cell coordinates are out of bounds.")
        return self.board[z][y][x]

    def print_board(self):
        """
        Debugging printout.
        Prints top layer first.
        """
        for z in range(self.height - 1, -1, -1):
            print(f"Layer z={z}")
            for y in range(self.rows):
                print(" ".join(str(self.board[z][y][x]) for x in range(self.cols)))
            print()

    def __str__(self):
        lines = []
        for z in range(self.height - 1, -1, -1):
            lines.append(f"Layer z={z}")
            for y in range(self.rows):
                lines.append(" ".join(str(self.board[z][y][x]) for x in range(self.cols)))
            lines.append("")
        return "\n".join(lines)