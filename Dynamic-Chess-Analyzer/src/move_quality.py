def classify_move(
    player_move,
    best_move,
    move_loss
):
    if best_move is not None:
        if player_move == best_move:
            return "Best Move"

    if move_loss <= 50:
        return "Good Move"

    if move_loss <= 150:
        return "Mistake"

    return "Blunder"