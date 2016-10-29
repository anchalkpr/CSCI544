import copy
from Board import Board

def alpha_beta_search(board, depth):
    best_move = None
    v = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    
    possible_moves = board.possible_moves(board.player, board.opponent)
    for move in possible_moves:
        moved_pieces = board.make_move(board.player, board.opponent, move[0], move[1])
        score = min_value(board, depth - 1, alpha, beta)
        board.remove_move(move[0], moved_pieces, board.opponent)
        if score > v:
            v = score
            best_move = move
                
        if v >= beta:
            best_move = move
            break
        alpha = max(alpha, v)

    board.make_move(board.player, board.opponent, best_move[0], best_move[1])
    return best_move, board.returnBoardState()
    
def min_value(board, depth, alpha, beta):
    if depth == 0 or board.game_over():
        return board.score()
    v = float('inf')
    possible_moves = board.possible_moves(board.opponent, board.player)
    for move in possible_moves:
        moved_pieces = board.make_move(board.opponent, board.player, move[0], move[1])
        score = max_value(board, depth - 1, alpha, beta)
        board.remove_move(move[0], moved_pieces, board.player)
        v = min(v, score)
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

def max_value(board, depth, alpha, beta):
    if depth == 0 or board.game_over():
        return board.score()
    v = float('-inf')
    possible_moves = board.possible_moves(board.player, board.opponent)
    for move in possible_moves:
        moved_pieces = board.make_move(board.player, board.opponent, move[0], move[1])
        score = min_value(board, depth - 1, alpha, beta)
        board.remove_move(move[0], moved_pieces, board.opponent)
        v = max(v, score)
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v