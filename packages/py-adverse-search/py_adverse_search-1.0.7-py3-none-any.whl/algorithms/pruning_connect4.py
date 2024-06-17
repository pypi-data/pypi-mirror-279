from .minimax_connect4 import minimax

def ai_turn(board, comp_piece, human_piece):
    """
    Determines and executes the best move for the AI using the minimax algorithm with alpha-beta pruning.

    :param board: The current state of the board.
    :param comp_piece: The piece representing the AI (COMP).
    :param human_piece: The piece representing the human player (HUMAN).
    """
    best_score = float('-inf')
    best_move = None
    for move in board.valid_moves():
        new_board = board.copy()
        new_board.drop_piece(move, comp_piece)
        score = minimax(new_board, 5, False, float('-inf'), float('inf'), comp_piece, human_piece)
        if score > best_score:
            best_score = score
            best_move = move
    board.drop_piece(best_move, comp_piece)
