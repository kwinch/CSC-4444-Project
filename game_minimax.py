from math import inf 
from game_state import Connect43D

AI = 2
HUMAN = 1
"""
rewards AI for better moves and Punish AI for bad moves 
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
    score = 0

    center_x = game.cols // 2
    center_y = game.rows // 2

    for z in range(game.height):
        for y in range(game.rows):
            for x in range(game.cols):
                piece = game.get_cell(x, y, z)

                if piece == AI:
                    score += 5 - abs(center_x - x)
                    score += 5 - abs(center_y -y)

                elif piece == HUMAN:
                    score -= 5 - abs(center_x - x)
                    score -= 5 - abs(center_y - y)

    return score



    
def minimax(game, depth, maximizing):
    # recursively checks furure moves and returns the best score
    if depth == 0 or game.get_winner() !=0 or game.is_full():
        return evaluate_board(game)
    
    if maximizing:
        best_score = -inf 
        for x, y in game.get_legal_moves():
            new_game = game.clone()
            new_game.make_move(x, y, AI)

            score = minimax(new_game, depth - 1, False)
            best_score = max(best_score, score)

        return best_score
    
    else:
        best_score = inf
        for x, y in game.get_legal_moves():
            new_game = game.clone()
            new_game.make_move(x, y, HUMAN)

            score = minimax(new_game, depth - 1 , True)
            best_score = min(best_score, score)

        return best_score
    
def get_best_move(game, depth=2):
    best_score = -inf
    best_move = None

    for x, y in game.get_legal_moves():
        new_game = game.clone()
        new_game.make_move(x, y, AI)

        score = minimax(new_game, depth - 1, False)

        if score > best_score:
            best_score = score 
            best_move = (x, y)

    return best_move
def ai_move(game, depth=2):
    move = get_best_move(game, depth)

    if move is None:
        return None
    
    x, y = move
    z = game.make_move(x, y, AI)

    return x, y, z

def test_minimax():
    game = Connect43D()
    print("Testing Minimax AI...")
    move = get_best_move(game, depth=2)
    print("Best move:", move)

    result = ai_move(game, depth=2)
    print(" AI move applied:", result)

if __name__ == "__main__":
    test_minimax()
