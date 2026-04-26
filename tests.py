from game_state import Connect43D


def test_basic_move():
    game = Connect43D()
    z = game.make_move(0, 0, player=1)
    assert z == 0
    assert game.get_cell(0, 0, 0) == 1
    assert game.winner == 0


def test_vertical_win():
    game = Connect43D()
    for _ in range(4):
        game.make_move(0, 0, player=1)
    assert game.winner == 1


def test_horizontal_win():
    game = Connect43D()
    for x in range(4):
        game.make_move(x, 0, player=1)
    assert game.winner == 1


def test_diagonal_xz_win():
    game = Connect43D()

    game.make_move(0, 0, player=1)

    game.make_move(1, 0, player=2)
    game.make_move(1, 0, player=1)

    game.make_move(2, 0, player=2)
    game.make_move(2, 0, player=2)
    game.make_move(2, 0, player=1)

    game.make_move(3, 0, player=2)
    game.make_move(3, 0, player=2)
    game.make_move(3, 0, player=2)
    game.make_move(3, 0, player=1)

    assert game.winner == 1


def test_draw_condition():
    game = Connect43D(height=1, rows=1, cols=1, connect_n=4)
    game.make_move(0, 0, player=1)
    assert game.winner == -1
    
def test_out_of_bounds():
    game = Connect43D()
    try:
        game.make_move(-1, 0, player=1)
        assert False
    except ValueError:
        pass

def stack_full():
    game = Connect43D(height=1, rows=1, cols=1)
    game.make_move(0, 0, player=1)
    try:
        game.make_move(0, 0, player=2)
        assert False
    except ValueError:
        pass

def turn_switching():
    game = Connect43D()
    game.make_move(0, 0)
    assert game.current_player == 2
    game.make_move(1, 0)
    assert game.current_player == 1

def undo_move():
    game = Connect43D()
    game.make_move(0, 0, player=1)
    game.undo_move()
    assert game.get_cell(0, 0, 0) == 0


if __name__ == "__main__":
    test_basic_move()
    test_vertical_win()
    test_horizontal_win()
    test_diagonal_xz_win()
    test_draw_condition()
    test_out_of_bounds()
    stack_full()
    turn_switching()
    undo_move()
    
    print("All tests passed.")