def board_to_fen(board):

    fen = ""

    for row in board:

        empty_count = 0

        for square in row:

            if square == "empty":

                empty_count += 1

            else:

                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0

                fen += square

        if empty_count > 0:
            fen += str(empty_count)

        fen += "/"

    fen = fen[:-1]

    # add side to move + castling etc.
    fen += " w KQkq - 0 1"

    return fen