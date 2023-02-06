import chess

def minimax(board, depth, is_maximizing):
    if depth == 0 or board.is_game_over():
        return board.result(), None

    if is_maximizing:
        best_value = -1000000
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            value, _ = minimax(board, depth - 1, False)
            board.pop()
            if value > best_value:
                best_value = value
                best_move = move
        return best_value, best_move
    else:
        best_value = 1000000
        best_move = None
        for move in board.legal_moves:
            board.push(move)
            value, _ = minimax(board, depth - 1, True)
            board.pop()
            if value < best_value:
                best_value = value
                best_move = move
        return best_value, best_move

board = chess.Board()
_, best_move = minimax(board, 4, True)
print(best_move)