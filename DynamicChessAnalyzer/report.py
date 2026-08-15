def save_move_report(move, best_move, evaluation, move_quality):
    with open("game_report.txt", "a") as file:
        file.write("Move Played: " + move + "\n")
        file.write("Stockfish Best Move: " + str(best_move) + "\n")
        file.write("Evaluation: " + str(evaluation) + "\n")
        file.write("Move Quality: " + str(move_quality) + "\n")
        file.write("-----------------------------------\n")