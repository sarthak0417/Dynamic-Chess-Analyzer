from demo_board import demo_board
from fen_generator import board_to_fen
from engine import get_best_move

fen = board_to_fen(demo_board)

print("Generated FEN:")
print(fen)

best_move, evaluation = get_best_move(fen)

print("\nBest Move:")
print(best_move)

print("\nEvaluation:")
print(evaluation)