import random

def simulate_random_game(board, piece):
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
