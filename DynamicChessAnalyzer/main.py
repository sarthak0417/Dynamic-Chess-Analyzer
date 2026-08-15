import cv2
import numpy as np

import engine
from grid import split_board
from pieces import detect_piece
from board_state import create_board_state, print_board_state
from move_detection import detect_move
from engine import get_best_move
from fen_generator import board_to_fen
from demo_board import demo_board
from game_manager import apply_move_and_analyze
from visualize import draw_best_move
from move_quality import classify_move
from report import save_move_report

fen = board_to_fen(demo_board)

best_move, evaluation = get_best_move(fen)

print("Stockfish Best Move:", best_move)
print("Evaluation:", evaluation)


points = []
captured_img = None


def mouse_click(event, x, y, flags, param):
    global points

    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append([x, y])
            print("Point selected:", x, y)


def order_points(pts):
    pts = np.array(pts, dtype="float32")

    rect = np.zeros((4, 2), dtype="float32")

    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    rect[0] = pts[np.argmin(s)]      # top-left
    rect[1] = pts[np.argmin(diff)]   # top-right
    rect[2] = pts[np.argmax(s)]      # bottom-right
    rect[3] = pts[np.argmax(diff)]   # bottom-left

    return rect


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
captured_img = None
previous_board_state = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    camera_display = frame.copy()

    cv2.imshow("Camera - ENTER capture | ESC exit", camera_display)

    key = cv2.waitKey(1)

    if key == 13:
        captured_img = frame.copy()
        points = []
        cv2.imshow("Captured Image - Click 4 board corners", captured_img)
        cv2.setMouseCallback("Captured Image - Click 4 board corners", mouse_click)
        print("Captured! Click 4 board corners.")

    if captured_img is not None:
        temp = captured_img.copy()

        for p in points:
            cv2.circle(temp, tuple(p), 7, (0, 0, 255), -1)

        cv2.imshow("Captured Image - Click 4 board corners", temp)

        if len(points) == 4:
            pts1 = order_points(points)

            pts2 = np.float32([
                [0, 0],
                [800, 0],
                [800, 800],
                [0, 800]
            ])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            warped = cv2.warpPerspective(captured_img, matrix, (800, 800))

            grid_view = warped.copy()
            square_size = 100

            for i in range(9):
                cv2.line(grid_view, (0, i * square_size), (800, i * square_size), (0, 255, 0), 1)
                cv2.line(grid_view, (i * square_size, 0), (i * square_size, 800), (0, 255, 0), 1)

            cv2.imshow("Warped Board", grid_view)

            squares, board_map = split_board(warped)

            board_state = create_board_state(board_map, detect_piece)
            print_board_state(board_state)

            if previous_board_state is not None:
                move = detect_move(previous_board_state, board_state)

                if move is not None:

                    from_sq, to_sq = move

                    print(f"Move detected: {from_sq} -> {to_sq}")

                    # -------- STOCKFISH ANALYSIS --------
                    uci_move = from_sq + to_sq

                    fen, best_move, evaluation = apply_move_and_analyze(uci_move)

                    print("Current FEN:", fen)

                    print("Stockfish Best Move:", best_move)

                    print("Evaluation:", evaluation)

                    # -------- MOVE QUALITY --------
                    move_quality = classify_move(uci_move, best_move, evaluation)

                    print("Move Quality:", move_quality)

                    # -------- SAVE REPORT --------
                    save_move_report(uci_move, best_move, evaluation, move_quality)

                    print("Report saved.")

                    # -------- VISUALIZE BEST MOVE --------
                    visual_board = warped.copy()

                    visual_board = draw_best_move(visual_board, best_move)

                    cv2.imshow("Best Move Visualization", visual_board)

                else:
                    print("No clear move detected")

            previous_board_state = board_state

            points = []

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()