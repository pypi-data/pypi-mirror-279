import random

def simulate_random_game(board, piece):
    """
    Simulates a random game from the given board state.

    :param board: The current state of the board.
    :param piece: The piece to start the simulation with (COMP or HUMAN).
    :return: 1 if COMP wins, -1 if HUMAN wins, 0 for a draw.
    """
    current_piece = piece
    while not board.game_over():
        valid_moves = board.valid_moves()
        move = random.choice(valid_moves)
        board.drop_piece(move, current_piece)
        current_piece = board.HUMAN if current_piece == board.COMP else board.COMP

    if board.wins(board.COMP):
        return 1
    elif board.wins(board.HUMAN):
        return -1
    else:
        return 0

def ai_turn(board, comp_piece, human_piece):
    """
    Makes a move for the AI using Monte Carlo simulation.

    :param board: The current state of the board.
    :param comp_piece: The piece representing the AI (COMP).
    :param human_piece: The piece representing the human player (HUMAN).
    """
    best_score = float('-inf')
    best_move = None

    for move in board.valid_moves():
        new_board = board.copy()
        new_board.drop_piece(move, comp_piece)
        score = sum(simulate_random_game(new_board.copy(), comp_piece) for _ in range(100)) / 100
        if score > best_score:
            best_score = score
            best_move = move
    if best_move is not None:
        board.drop_piece(best_move, comp_piece)
