def create_board_state(board_map, detect_piece):
    board_state = []

    ranks = [8, 7, 6, 5, 4, 3, 2, 1]
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    for rank in ranks:
        row = []

        for file in files:
            square_name = file + str(rank)
            square_image = board_map[square_name]

            result = detect_piece(square_image)

            row.append(result)

        board_state.append(row)

    return board_state


def print_board_state(board_state):
    print("\nCurrent Board State:")
    print("--------------------")

    for row in board_state:
        print(row)