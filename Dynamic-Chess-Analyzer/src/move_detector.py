import chess

from src.config import DIFF_THRESHOLD


def expected_changed_squares(
    board,
    move
):
    changed = {
        chess.square_name(
            move.from_square
        ),
        chess.square_name(
            move.to_square
        ),
    }

    if board.is_castling(move):

        rank = "1"

        if board.turn == chess.BLACK:
            rank = "8"

        if board.is_kingside_castling(move):
            changed.add("h" + rank)
            changed.add("f" + rank)

        else:
            changed.add("a" + rank)
            changed.add("d" + rank)

    if board.is_en_passant(move):

        if board.turn == chess.WHITE:
            captured_square = (
                move.to_square - 8
            )

        else:
            captured_square = (
                move.to_square + 8
            )

        changed.add(
            chess.square_name(
                captured_square
            )
        )

    return changed


def infer_move(
    board,
    difference_scores
):
    observed_squares = [
        square
        for square, score
        in difference_scores.items()
        if score >= DIFF_THRESHOLD
    ]

    observed_squares.sort(
        key=lambda square:
        difference_scores[square],
        reverse=True
    )

    best_move = None
    best_confidence = float("-inf")

    for move in board.legal_moves:

        expected = expected_changed_squares(
            board,
            move
        )

        expected_scores = [
            difference_scores.get(
                square,
                0
            )
            for square in expected
        ]

        if not expected_scores:
            continue

        expected_average = (
            sum(expected_scores) /
            len(expected_scores)
        )

        expected_minimum = min(
            expected_scores
        )

        outside_scores = [
            score
            for square, score
            in difference_scores.items()
            if square not in expected
        ]

        outside_scores.sort(
            reverse=True
        )

        outside_average = 0

        if outside_scores:
            sample = outside_scores[
                :len(expected)
            ]

            outside_average = (
                sum(sample) /
                len(sample)
            )

        confidence = (
            expected_average -
            (0.35 * outside_average)
        )

        if (
            expected_minimum <
            DIFF_THRESHOLD * 0.5
        ):
            confidence -= DIFF_THRESHOLD

        if confidence > best_confidence:
            best_confidence = confidence
            best_move = move

    if best_move is None:
        return None, observed_squares, 0

    if best_confidence < (
        DIFF_THRESHOLD * 0.25
    ):
        return (
            None,
            observed_squares,
            best_confidence
        )

    return (
        best_move,
        observed_squares,
        best_confidence
    )