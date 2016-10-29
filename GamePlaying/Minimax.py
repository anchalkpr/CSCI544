from Board import Board
import copy

def minimax_decision(board, depth):
    v = float('-inf')
    node = None
    possible_moves = board.possible_moves(board.player, board.opponent)
    for move in possible_moves:
        moved_pieces = board.make_move(board.player, board.opponent, move[0], move[1])
        score = min_value(board, depth - 1)
        board.remove_move(move[0], moved_pieces, board.opponent)
        if score > v:
            v = score
            node = move
    
    board.make_move(board.player, board.opponent, node[0], node[1])       
    return node, board.returnBoardState()
    
def min_value(board, depth):
    if depth == 0 or board.game_over():
        return board.score()
    v = float('inf')
    possible_moves = board.possible_moves(board.opponent, board.player)
    for move in possible_moves:
        moved_pieces = board.make_move(board.opponent, board.player, move[0], move[1])
        score = max_value(board, depth - 1)
        board.remove_move(move[0], moved_pieces, board.player)
        v = min(score, v)
    return v

def max_value(board, depth):
    if depth == 0 or board.game_over():
        return board.score()
    v = float('-inf')
    possible_moves = board.possible_moves(board.player, board.opponent)
    for move in possible_moves:
        moved_pieces = board.make_move(board.player, board.opponent, move[0], move[1])
        score = min_value(board, depth - 1)
        board.remove_move(move[0], moved_pieces, board.opponent)
        v = max(v, score)
    return v   