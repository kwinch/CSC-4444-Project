from game_state import Connect43D


def run_game():
    game = Connect43D()

    print("3D Connect 4")
    print("Enter moves as: x y")
    print("x = column, y = row")
    print("Type 'q' to quit.\n")

    while game.winner == 0:
        print(game)
        print(f"Player {game.current_player}'s turn")

        raw = input("Move: ").strip().lower()

        if raw in {"q", "quit", "exit"}:
            print("Game ended by user.")
            return

        try:
            parts = raw.split()
            if len(parts) != 2:
                raise ValueError("Enter exactly two numbers: x y")

            x = int(parts[0])
            y = int(parts[1])

            z = game.make_move(x, y)
            print(f"Placed at (x={x}, y={y}, z={z})\n")

        except Exception as e:
            print(f"Invalid move: {e}\n")

    print(game)

    if game.winner == -1:
        print("Draw!")
    else:
        print(f"Player {game.winner} wins!")


if __name__ == "__main__":
    run_game()