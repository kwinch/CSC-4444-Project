from game_state import Connect43D
from game_minimax import get_best_move

def run_game():
    game = Connect43D()

    print("3D Connect 4")
    print("Enter moves as: x y")
    print("x = column, y = row")
    print("Type 'q' to quit.\n")

    while game.winner == 0:
        print(game)


        if game.current_player == 1:
            print("Your turn (Player 1)")
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

                z = game.make_move(x, y, 1)
                print(f"Placed at (x={x}, y={y}, z={z})\n")
            

            except Exception as e:
                print(f"Invalid move: {e}\n")
        
        else:
            print ("Player 2 is thinking...")
            move = get_best_move(game, depth=2)

            if move is None:
                print("No vaild move for Player 2.")
                return
            
            x, y = move 
            z = game.make_move(x, y, 2)
            print(f"Player 2 played: x={x}, y={y}, z={z}\n")

    print(game)

    if game.winner == -1:
        print("Draw!")
    else:
        print(f"Player {game.winner} wins!")


#if __name__ == "__main__":
    #run_game()