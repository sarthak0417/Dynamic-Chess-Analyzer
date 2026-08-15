import cv2

BOARD_SIZE = 800
GRID_SIZE = 8
SQUARE_SIZE = BOARD_SIZE // GRID_SIZE

def split_board(board):
    board = cv2.resize(board, (BOARD_SIZE, BOARD_SIZE))

    squares = []
    board_map = {}

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE
            x2 = (col + 1) * SQUARE_SIZE
            y2 = (row + 1) * SQUARE_SIZE

            square = board[y1:y2, x1:x2]

            square_name = files[col] + str(8 - row)

            squares.append(square)
            board_map[square_name] = square

    return squares, board_map