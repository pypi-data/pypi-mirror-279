from math import inf as infinity
from random import choice
import time

def minimax(game, state, depth, player):
    """
    AI function that chooses the best move

    :param game: instance of the tictactoe class
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see ai_turn() function)
    :param player: a human or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == game.COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game.game_over(state):
        score = game.evaluate(state)
        return [-1, -1, score]
    for cell in game.empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(game, state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == game.COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best

def ai_turn(game, c_choice, h_choice):
    """
    It calls the minimax function if the depth < 9,
    else it chooses a random coordinate.

    :param game: instance of the tictactoe class
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(game.empty_cells(game.board))
    if depth == 0 or game.game_over(game.board):
        return

    game.clean()
    print(f'Computer turn [{c_choice}]')
    game.render(game.board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(game, game.board, depth, game.COMP)
        x, y = move[0], move[1]

    game.set_move(x, y, game.COMP)
    time.sleep(1)
    