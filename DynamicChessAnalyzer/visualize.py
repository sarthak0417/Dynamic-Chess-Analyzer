import cv2

def square_to_coords(square):

    files = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }

    file = square[0]
    rank = int(square[1])

    col = files[file]
    row = 8 - rank

    x = col * 100 + 50
    y = row * 100 + 50

    return (x, y)


def draw_best_move(board_image, move):

    if move is None:
        return board_image

    from_sq = move[:2]
    to_sq = move[2:]

    start = square_to_coords(from_sq)
    end = square_to_coords(to_sq)

    cv2.arrowedLine(
        board_image,
        start,
        end,
        (0, 0, 255),
        5,
        tipLength=0.3
    )

    return board_image