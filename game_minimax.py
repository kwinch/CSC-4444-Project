from math import inf 
from game_state import Connect43D

AI = 2
HUMAN = 1
"""
looks at the board to see who won
"""
def evaluate_board(game):
    winner = game.get_winner()

    if winner == AI:
        return 100000
    elif winner == HUMAN:
        return -100000
    elif winner == -1:
        return 0
    else:
        return 0
    
def minimax(game, depth, maximizing):
    if depth == 0 or game.get_winner() !=0 or game.is_full():
        return evaluate_board(game)
    if maximizing:
        best_score = -inf 
        for x, y in game.get_legal_moves():
            new_game = game.clone()
            new_game.make_move(x, y, AI)
            score = minimax(new_game, depth -1, False)
            best_score = max(best_score, score)

        return best_score
    else:
        best_score = inf
        for x, y in game.get_legal_moves():
            new_game = game.clone()
            new_game.make_move(x, y, AI)
            score = minimax(new_game, depth-1 ,False)
            best_score = max(best_score, score)

        return best_score
    
def get_best_move(game, depth=3):
    best_score = -inf
    best_move = None

    for x, y in game.get_legal_moves():
        new_game = game.clone()
        new_game.make_move(x, y, AI)
        score = minimax(new_game, depth -1, False )
        if score > best_score:
            best_score = score 
            best_move = (x, y)

    return best_move

def test_minimax();
    game = Connect43D
    print("Testing Minimax AI...")
    move = get_best_move(game, depth=2)
    print("Best move:", move)

if __name__ == "__main__":
    test_minimax()
