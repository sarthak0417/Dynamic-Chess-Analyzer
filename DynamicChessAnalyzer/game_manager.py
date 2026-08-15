import chess
from engine import get_best_move

board = chess.Board()

def apply_move_and_analyze(move_text):
    global board

    try:
        move = chess.Move.from_uci(move_text)

        if move not in board.legal_moves:
            return "Illegal move", None, None

        board.push(move)

        fen = board.fen()

        best_move, evaluation = get_best_move(fen)

        return fen, best_move, evaluation

    except Exception as e:
        return f"Error: {e}", None, None