from stockfish import Stockfish

STOCKFISH_PATH = r"C:\Users\hp\OneDrive\เอกสาร\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"

stockfish = Stockfish(STOCKFISH_PATH)

def get_best_move(fen):

    stockfish.set_fen_position(fen)

    best_move = stockfish.get_best_move()

    evaluation = stockfish.get_evaluation()

    return best_move, evaluation