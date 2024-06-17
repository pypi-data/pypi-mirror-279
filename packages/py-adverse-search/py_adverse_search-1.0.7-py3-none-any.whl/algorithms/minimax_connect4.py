def minimax(board, depth, maximizing_player, alpha, beta, comp_piece, human_piece):
    """
    Implements the minimax algorithm with alpha-beta pruning.

    :param board: The current state of the board.
    :param depth: The maximum depth to search.
    :param maximizing_player: True if the current move is for the maximizing player (COMP).
    :param alpha: The best value that the maximizer currently can guarantee.
    :param beta: The best value that the minimizer currently can guarantee.
    :param comp_piece: The piece representing the AI (COMP).
    :param human_piece: The piece representing the human player (HUMAN).
    :return: The evaluated score of the board.
    """
    if board.game_over() or depth == 0:
        if board.wins(comp_piece):
            return 1
        elif board.wins(human_piece):
            return -1
        else:
            return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.valid_moves():
            new_board = board.copy()
            new_board.drop_piece(move, comp_piece)
            eval = minimax(new_board, depth - 1, False, alpha, beta, comp_piece, human_piece)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.valid_moves():
            new_board = board.copy()
            new_board.drop_piece(move, human_piece)
            eval = minimax(new_board, depth - 1, True, alpha, beta, comp_piece, human_piece)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def ai_turn(board, comp_piece, human_piece):
    """
    Determines and executes the best move for the AI using the minimax algorithm.

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
    if best_move is not None:
        board.drop_piece(best_move, comp_piece)
