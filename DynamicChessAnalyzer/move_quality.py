def classify_move(player_move, best_move, evaluation):
    if player_move == best_move:
        return "Best Move"

    if evaluation is None:
        return "Unknown"

    if evaluation["type"] == "cp":
        score = abs(evaluation["value"])

        if score <= 50:
            return "Good Move"
        elif score <= 150:
            return "Mistake"
        else:
            return "Blunder"

    if evaluation["type"] == "mate":
        return "Critical Move"

    return "Unknown"