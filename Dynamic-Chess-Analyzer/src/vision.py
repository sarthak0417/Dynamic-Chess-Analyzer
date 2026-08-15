import cv2
import numpy as np
import chess

from src.config import (
    BOARD_SIZE,
    GRID_SIZE,
    SQUARE_SIZE,
)


FILES = "abcdefgh"


def order_points(points):
    points = np.array(
        points,
        dtype="float32"
    )

    rect = np.zeros(
        (4, 2),
        dtype="float32"
    )

    point_sum = points.sum(axis=1)

    point_diff = np.diff(
        points,
        axis=1
    ).reshape(-1)

    rect[0] = points[
        np.argmin(point_sum)
    ]

    rect[2] = points[
        np.argmax(point_sum)
    ]

    rect[1] = points[
        np.argmin(point_diff)
    ]

    rect[3] = points[
        np.argmax(point_diff)
    ]

    return rect


def create_warp_matrix(points):
    source = order_points(points)

    destination = np.float32([
        [0, 0],
        [BOARD_SIZE, 0],
        [BOARD_SIZE, BOARD_SIZE],
        [0, BOARD_SIZE],
    ])

    matrix = cv2.getPerspectiveTransform(
        source,
        destination
    )

    return matrix


def warp_frame(frame, matrix):
    return cv2.warpPerspective(
        frame,
        matrix,
        (BOARD_SIZE, BOARD_SIZE)
    )


def draw_grid(board_image):
    output = board_image.copy()

    for i in range(GRID_SIZE + 1):
        position = i * SQUARE_SIZE

        cv2.line(
            output,
            (0, position),
            (BOARD_SIZE, position),
            (0, 255, 0),
            1
        )

        cv2.line(
            output,
            (position, 0),
            (position, BOARD_SIZE),
            (0, 255, 0),
            1
        )

    return output


def split_squares(board_image):
    squares = {}

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):

            x1 = col * SQUARE_SIZE
            y1 = row * SQUARE_SIZE

            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE

            square_image = board_image[
                y1:y2,
                x1:x2
            ]

            square_name = (
                FILES[col] +
                str(8 - row)
            )

            squares[square_name] = (
                square_image
            )

    return squares


def square_difference_scores(
    previous_board,
    current_board
):
    previous_squares = split_squares(
        previous_board
    )

    current_squares = split_squares(
        current_board
    )

    scores = {}

    for square_name in previous_squares:

        previous = previous_squares[
            square_name
        ]

        current = current_squares[
            square_name
        ]

        previous_gray = cv2.cvtColor(
            previous,
            cv2.COLOR_BGR2GRAY
        )

        current_gray = cv2.cvtColor(
            current,
            cv2.COLOR_BGR2GRAY
        )

        previous_gray = cv2.GaussianBlur(
            previous_gray,
            (5, 5),
            0
        )

        current_gray = cv2.GaussianBlur(
            current_gray,
            (5, 5),
            0
        )

        difference = cv2.absdiff(
            previous_gray,
            current_gray
        )

        scores[square_name] = float(
            np.mean(difference)
        )

    return scores


def square_center(square_name):
    file_index = FILES.index(
        square_name[0]
    )

    rank = int(
        square_name[1]
    )

    row = 8 - rank
    col = file_index

    x = (
        col * SQUARE_SIZE +
        SQUARE_SIZE // 2
    )

    y = (
        row * SQUARE_SIZE +
        SQUARE_SIZE // 2
    )

    return x, y


def draw_move_arrow(
    board_image,
    move
):
    output = board_image.copy()

    if move is None:
        return output

    from_square = chess.square_name(
        move.from_square
    )

    to_square = chess.square_name(
        move.to_square
    )

    start = square_center(
        from_square
    )

    end = square_center(
        to_square
    )

    cv2.arrowedLine(
        output,
        start,
        end,
        (0, 0, 255),
        7,
        tipLength=0.25
    )

    return output