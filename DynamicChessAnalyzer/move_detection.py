def index_to_square(row, col):
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    rank = 8 - row
    return files[col] + str(rank)


def detect_move(previous_state, current_state):
    changed_squares = []

    for row in range(8):
        for col in range(8):
            if previous_state[row][col] != current_state[row][col]:
                changed_squares.append((row, col))

    if len(changed_squares) == 2:
        sq1 = changed_squares[0]
        sq2 = changed_squares[1]

        r1, c1 = sq1
        r2, c2 = sq2

        # from square usually becomes empty
        if current_state[r1][c1] == "empty":
            from_square = index_to_square(r1, c1)
            to_square = index_to_square(r2, c2)
        else:
            from_square = index_to_square(r2, c2)
            to_square = index_to_square(r1, c1)

        return from_square, to_square

    return None