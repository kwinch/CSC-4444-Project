from __future__ import annotations

from dataclasses import dataclass
from math import inf
from typing import Iterable, List, Optional, Sequence, Tuple


Move = Tuple[int, int]


@dataclass(frozen=True)
class SearchResult:
    # `move` is the best row/column stack found by the search.
    # `score` is the heuristic value of that move sequence.
    move: Optional[Move]
    score: int


class Connect43D:
    def __init__(self, height: int = 6, rows: int = 6, cols: int = 7) -> None:
        self.height = height
        self.rows = rows
        self.cols = cols
        # The board is indexed as board[height][row][col].
        # A value of 0 means empty, 1 means player one, and 2 means player two.
        self.board = [
            [[0 for _ in range(cols)] for _ in range(rows)]
            for _ in range(height)
        ]
        # Precompute all search directions and every possible 4-cell winning line
        # so the game does not have to rebuild them during the AI search.
        self.directions = self._build_directions()
        self.lines = self._build_lines()

    def copy(self) -> "Connect43D":
        # Create a completely separate board state for experiments or testing.
        clone = Connect43D(self.height, self.rows, self.cols)
        clone.board = [
            [row[:] for row in level]
            for level in self.board
        ]
        return clone

    def _build_directions(self) -> Sequence[Tuple[int, int, int]]:
        # We keep only one version of each direction to avoid counting
        # the same line twice in opposite directions.
        directions = []
        for dh in (-1, 0, 1):
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dh == dr == dc == 0:
                        continue
                    if (dh, dr, dc) > (0, 0, 0):
                        directions.append((dh, dr, dc))
        return directions

    def _build_lines(self) -> List[List[Tuple[int, int, int]]]:
        # Build every possible 4-cell line on the board one time.
        # This lets winner detection and board evaluation loop over a fixed list.
        lines: List[List[Tuple[int, int, int]]] = []
        seen = set()

        for h in range(self.height):
            for r in range(self.rows):
                for c in range(self.cols):
                    for dh, dr, dc in self.directions:
                        line = []
                        for step in range(4):
                            nh = h + dh * step
                            nr = r + dr * step
                            nc = c + dc * step
                            if not self.in_bounds(nh, nr, nc):
                                line = []
                                break
                            line.append((nh, nr, nc))
                        if len(line) == 4:
                            key = tuple(sorted(line))
                            if key not in seen:
                                seen.add(key)
                                lines.append(line)
        return lines

    def in_bounds(self, h: int, r: int, c: int) -> bool:
        return 0 <= h < self.height and 0 <= r < self.rows and 0 <= c < self.cols

    def legal_moves(self) -> List[Move]:
        # A stack is playable if its top cell is still empty.
        return [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self.board[self.height - 1][r][c] == 0
        ]

    def make_move(self, row: int, col: int, player: int) -> Optional[int]:
        # A move drops into the lowest empty height position of a row/column stack.
        for h in range(self.height):
            if self.board[h][row][col] == 0:
                self.board[h][row][col] = player
                return h
        return None

    def undo_move(self, row: int, col: int) -> None:
        # Undo removes the topmost piece from the chosen stack.
        # The search uses this after trying a hypothetical move.
        for h in range(self.height - 1, -1, -1):
            if self.board[h][row][col] != 0:
                self.board[h][row][col] = 0
                return
        raise ValueError("Cannot undo move from an empty column stack.")

    def is_full(self) -> bool:
        return all(self.board[self.height - 1][r][c] != 0 for r in range(self.rows) for c in range(self.cols))

    def winner(self) -> int:
        # Check every precomputed winning line and see whether all four cells
        # belong to the same non-empty player.
        for line in self.lines:
            values = [self.board[h][r][c] for h, r, c in line]
            if values[0] != 0 and all(value == values[0] for value in values[1:]):
                return values[0]
        return 0

    def evaluate_window(self, values: Iterable[int], ai_player: int) -> int:
        # Score one 4-cell line from the AI's point of view.
        # Positive values help the AI, negative values help the opponent.
        values = list(values)
        opponent = 1 if ai_player == 2 else 2

        ai_count = values.count(ai_player)
        opp_count = values.count(opponent)
        empty_count = values.count(0)

        # Winning and losing lines get the strongest scores so the search
        # strongly prefers forced wins and blocks immediate losses.
        if ai_count == 4:
            return 100000
        if opp_count == 4:
            return -100000

        # Partial lines are weighted by how close they are to becoming four-in-a-row.
        if ai_count == 3 and empty_count == 1:
            return 120
        if ai_count == 2 and empty_count == 2:
            return 12
        if ai_count == 1 and empty_count == 3:
            return 1

        if opp_count == 3 and empty_count == 1:
            return -150
        if opp_count == 2 and empty_count == 2:
            return -15
        if opp_count == 1 and empty_count == 3:
            return -1

        return 0

    def evaluate(self, ai_player: int) -> int:
        # This is the board heuristic used when the search stops before
        # reaching a terminal win/loss position.
        total = 0
        center_row = self.rows // 2
        center_col = self.cols // 2

        # Prefer central stacks because they usually participate in more lines.
        for h in range(self.height):
            for r in range(self.rows):
                for c in range(self.cols):
                    piece = self.board[h][r][c]
                    if piece == ai_player:
                        total += 4 - abs(center_row - r)
                        total += 4 - abs(center_col - c)
                    elif piece != 0:
                        total -= 4 - abs(center_row - r)
                        total -= 4 - abs(center_col - c)

        # Add the contribution from every possible 4-cell winning window.
        for line in self.lines:
            window = [self.board[h][r][c] for h, r, c in line]
            total += self.evaluate_window(window, ai_player)

        return total


class AlphaBetaAI:
    def __init__(self, ai_player: int = 2, max_depth: int = 3) -> None:
        # `max_depth` controls how many turns ahead the AI explores.
        # Higher depth is stronger but slower.
        self.ai_player = ai_player
        self.human_player = 1 if ai_player == 2 else 2
        self.max_depth = max_depth

    def choose_move(self, game: Connect43D) -> SearchResult:
        # Start the search from the AI turn as a maximizing player.
        result = self._alphabeta(
            game=game,
            depth=self.max_depth,
            alpha=-inf,
            beta=inf,
            maximizing=True,
        )
        return result

    def _alphabeta(
        self,
        game: Connect43D,
        depth: int,
        alpha: float,
        beta: float,
        maximizing: bool,
    ) -> SearchResult:
        # First handle terminal conditions: win, loss, draw, or search depth limit.
        winner = game.winner()
        if winner == self.ai_player:
            return SearchResult(None, 1_000_000 + depth)
        if winner == self.human_player:
            return SearchResult(None, -1_000_000 - depth)
        if depth == 0 or game.is_full():
            return SearchResult(None, game.evaluate(self.ai_player))

        # Try more promising moves first so alpha-beta can prune more branches.
        moves = self._ordered_moves(game)
        if not moves:
            return SearchResult(None, 0)

        if maximizing:
            # The AI wants the highest score it can force.
            best_score = -inf
            best_move: Optional[Move] = moves[0]
            for row, col in moves:
                # Apply the move, search the reply, then undo the move.
                game.make_move(row, col, self.ai_player)
                score = self._alphabeta(game, depth - 1, alpha, beta, False).score
                game.undo_move(row, col)

                if score > best_score:
                    best_score = score
                    best_move = (row, col)

                # Update the best guaranteed score for the maximizing side.
                alpha = max(alpha, best_score)
                # If this branch is already too good for the minimizing side to allow,
                # there is no need to search the remaining sibling moves.
                if beta <= alpha:
                    break

            return SearchResult(best_move, int(best_score))

        # The opponent turn is the minimizing side, so it looks for the lowest score.
        best_score = inf
        best_move = moves[0]
        for row, col in moves:
            game.make_move(row, col, self.human_player)
            score = self._alphabeta(game, depth - 1, alpha, beta, True).score
            game.undo_move(row, col)

            if score < best_score:
                best_score = score
                best_move = (row, col)

            # Update the best guaranteed score for the minimizing side.
            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return SearchResult(best_move, int(best_score))

    def _ordered_moves(self, game: Connect43D) -> List[Move]:
        # Move ordering improves alpha-beta pruning.
        # Central stacks are searched first because they are often stronger moves.
        center_row = game.rows / 2
        center_col = game.cols / 2
        moves = game.legal_moves()
        moves.sort(key=lambda move: abs(move[0] - center_row) + abs(move[1] - center_col))
        return moves


def print_top_view(game: Connect43D) -> None:
    # This helper prints the highest visible piece in each stack.
    # It is useful for debugging, even though the full board is 3D.
    for r in range(game.rows):
        cells = []
        for c in range(game.cols):
            symbol = "."
            for h in range(game.height - 1, -1, -1):
                if game.board[h][r][c] == 1:
                    symbol = "X"
                    break
                if game.board[h][r][c] == 2:
                    symbol = "O"
                    break
            cells.append(symbol)
        print(" ".join(cells))
    print()


def demo() -> None:
    # Create a sample game state and ask the AI for the best reply.
    game = Connect43D(height=6, rows=6, cols=7)
    ai = AlphaBetaAI(ai_player=2, max_depth=3)

    # Sample position before the AI move.
    opening_moves = [
        (4, 3, 1),
        (2, 3, 2),
        (5, 4, 1),
        (3, 3, 2),
        (1, 3, 1),
        (3, 4, 2),
    ]
    for row, col, player in opening_moves:
        game.make_move(row, col, player)

    print("Current top view:")
    print_top_view(game)

    result = ai.choose_move(game)
    print(f"Best move for AI: {result.move}, score={result.score}")


if __name__ == "__main__":
    demo()
