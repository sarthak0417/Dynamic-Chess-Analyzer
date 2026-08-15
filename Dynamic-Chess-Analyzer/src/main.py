import cv2
import chess

from src.config import CAMERA_INDEX

from src.engine import (
    start_engine,
    analyze_position,
    score_to_centipawns,
)

from src.move_quality import (
    classify_move,
)

from src.vision import (
    create_warp_matrix,
    warp_frame,
    draw_grid,
    square_difference_scores,
    draw_move_arrow,
)

from src.move_detector import (
    infer_move,
)

from src.report import (
    save_game_report,
)


selected_points = []


def mouse_callback(
    event,
    x,
    y,
    flags,
    param
):
    if (
        event ==
        cv2.EVENT_LBUTTONDOWN
    ):
        if len(selected_points) < 4:

            selected_points.append(
                (x, y)
            )

            print(
                "Corner selected:",
                x,
                y
            )


def capture_calibration_frame(
    camera
):
    print(
        "\nCamera opened."
    )

    print(
        "Place the chessboard in view."
    )

    print(
        "Press ENTER to capture calibration frame."
    )

    print(
        "Press Q to quit."
    )

    while True:

        success, frame = camera.read()

        if not success:
            return None

        display = frame.copy()

        cv2.putText(
            display,
            "ENTER = Capture | Q = Quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Dynamic Chess Analyzer",
            display
        )

        key = cv2.waitKey(1) & 0xFF

        if key == 13:
            return frame.copy()

        if key == ord("q"):
            return None


def select_board_corners(
    frame
):
    global selected_points

    selected_points = []

    window_name = (
        "Select 4 Chessboard Corners"
    )

    cv2.namedWindow(
        window_name
    )

    cv2.setMouseCallback(
        window_name,
        mouse_callback
    )

    print(
        "\nClick the four OUTER corners "
        "of the chessboard."
    )

    print(
        "You can click them in any order."
    )

    print(
        "Press R to reset."
    )

    print(
        "Press ENTER when 4 points are selected."
    )

    while True:

        display = frame.copy()

        for point in selected_points:

            cv2.circle(
                display,
                point,
                7,
                (0, 0, 255),
                -1
            )

        cv2.imshow(
            window_name,
            display
        )

        key = cv2.waitKey(20) & 0xFF

        if key == ord("r"):
            selected_points = []

        if (
            key == 13 and
            len(selected_points) == 4
        ):
            cv2.destroyWindow(
                window_name
            )

            return selected_points.copy()

        if key == ord("q"):
            cv2.destroyWindow(
                window_name
            )

            return None


def capture_move_frame(
    camera
):
    print(
        "\nMake the physical chess move."
    )

    print(
        "Remove your hand from the board."
    )

    print(
        "Press C to capture the new board."
    )

    print(
        "Press Q to stop the game."
    )

    while True:

        success, frame = camera.read()

        if not success:
            return None

        display = frame.copy()

        cv2.putText(
            display,
            "C = Capture Move | Q = Quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Dynamic Chess Analyzer",
            display
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            return frame.copy()

        if key == ord("q"):
            return None


def main():
    board = chess.Board()

    move_history = []

    camera = cv2.VideoCapture(
        CAMERA_INDEX,
        cv2.CAP_MSMF
    )

    if not camera.isOpened():
        print("MSMF camera backend failed. Trying default backend...")

        camera.release()

        camera = cv2.VideoCapture(
            CAMERA_INDEX
        )

    if not camera.isOpened():

        print(
            "Could not open webcam."
        )

        return

    engine = None

    try:
        engine = start_engine()

        print(
            "\n=============================="
        )

        print(
            "   DYNAMIC CHESS ANALYZER"
        )

        print(
            "=============================="
        )

        calibration_frame = (
            capture_calibration_frame(
                camera
            )
        )

        if calibration_frame is None:
            return

        points = select_board_corners(
            calibration_frame
        )

        if points is None:
            return

        matrix = create_warp_matrix(
            points
        )

        previous_board_image = (
            warp_frame(
                calibration_frame,
                matrix
            )
        )

        cv2.imshow(
            "Calibrated Chessboard",
            draw_grid(
                previous_board_image
            )
        )

        cv2.waitKey(1000)

        print(
            "\nCalibration completed."
        )

        print(
            "IMPORTANT:"
        )

        print(
            "The physical board must start "
            "from the normal chess position."
        )

        while not board.is_game_over():

            player = board.turn

            player_name = (
                "White"
                if player == chess.WHITE
                else "Black"
            )

            before_result = (
                analyze_position(
                    engine,
                    board,
                    perspective=player
                )
            )

            best_move = (
                before_result[
                    "best_move"
                ]
            )

            before_cp = (
                score_to_centipawns(
                    before_result[
                        "score"
                    ]
                )
            )

            print(
                "\n------------------------------"
            )

            print(
                "Turn:",
                player_name
            )

            print(
                "Stockfish best move:",
                best_move
            )

            print(
                "Evaluation:",
                before_cp,
                "cp"
            )

            recommendation = (
                draw_move_arrow(
                    previous_board_image,
                    best_move
                )
            )

            recommendation = (
                draw_grid(
                    recommendation
                )
            )

            cv2.imshow(
                "Stockfish Recommendation",
                recommendation
            )

            new_frame = capture_move_frame(
                camera
            )

            if new_frame is None:
                print(
                    "\nGame stopped by user."
                )

                break

            current_board_image = (
                warp_frame(
                    new_frame,
                    matrix
                )
            )

            difference_scores = (
                square_difference_scores(
                    previous_board_image,
                    current_board_image
                )
            )

            detected_move, changed_squares, confidence = (
                infer_move(
                    board,
                    difference_scores
                )
            )

            print(
                "\nChanged squares:",
                changed_squares
            )

            print(
                "Detection confidence:",
                round(
                    confidence,
                    2
                )
            )

            if detected_move is None:

                print(
                    "Move could not be detected "
                    "confidently."
                )

                manual_move = input(
                    "Type the UCI move manually "
                    "or press ENTER to retry: "
                ).strip()

                if not manual_move:
                    continue

                try:
                    detected_move = (
                        chess.Move.from_uci(
                            manual_move
                        )
                    )

                except ValueError:

                    print(
                        "Invalid UCI move."
                    )

                    continue

                if (
                    detected_move not in
                    board.legal_moves
                ):

                    print(
                        "Illegal move."
                    )

                    continue

            print(
                "Detected move:",
                detected_move
            )

            best_position = (
                board.copy()
            )

            if best_move is not None:

                best_position.push(
                    best_move
                )

                best_after_result = (
                    analyze_position(
                        engine,
                        best_position,
                        perspective=player
                    )
                )

                best_after_cp = (
                    score_to_centipawns(
                        best_after_result[
                            "score"
                        ]
                    )
                )

            else:
                best_after_cp = (
                    before_cp
                )

            board.push(
                detected_move
            )

            actual_after_result = (
                analyze_position(
                    engine,
                    board,
                    perspective=player
                )
            )

            actual_after_cp = (
                score_to_centipawns(
                    actual_after_result[
                        "score"
                    ]
                )
            )

            move_loss = max(
                0,
                best_after_cp -
                actual_after_cp
            )

            move_quality = (
                classify_move(
                    detected_move,
                    best_move,
                    move_loss
                )
            )

            print(
                "\nMove played:",
                detected_move
            )

            print(
                "Move quality:",
                move_quality
            )

            print(
                "Best-line evaluation:",
                best_after_cp,
                "cp"
            )

            print(
                "Actual evaluation:",
                actual_after_cp,
                "cp"
            )

            print(
                "Centipawn loss:",
                move_loss
            )

            print(
                "FEN:",
                board.fen()
            )

            move_history.append({
                "move_number":
                    len(move_history) + 1,

                "player":
                    player_name,

                "move":
                    str(
                        detected_move
                    ),

                "best_move":
                    (
                        str(best_move)
                        if best_move
                        else None
                    ),

                "quality":
                    move_quality,

                "centipawn_loss":
                    move_loss,

                "evaluation_before":
                    before_cp,

                "evaluation_after":
                    actual_after_cp,

                "fen":
                    board.fen(),
            })

            previous_board_image = (
                current_board_image
            )

            result_image = (
                draw_grid(
                    current_board_image
                )
            )

            cv2.putText(
                result_image,
                (
                    f"{detected_move} - "
                    f"{move_quality}"
                ),
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

            cv2.imshow(
                "Move Result",
                result_image
            )

            cv2.waitKey(500)

        print(
            "\n=============================="
        )

        print(
            "GAME FINISHED"
        )

        print(
            "=============================="
        )

        print(
            "Result:",
            (
                board.result()
                if board.is_game_over()
                else "Stopped"
            )
        )

        print(
            "\nMove History"
        )

        print(
            "------------"
        )

        for record in move_history:

            print(
                f"{record['move_number']}. "
                f"{record['player']} "
                f"{record['move']} "
                f"- {record['quality']} "
                f"- {record['centipawn_loss']} cp"
            )

        json_path, pgn_path = (
            save_game_report(
                move_history,
                board
            )
        )

        print(
            "\nJSON report saved:"
        )

        print(
            json_path
        )

        print(
            "\nPGN saved:"
        )

        print(
            pgn_path
        )

    finally:

        if engine is not None:
            engine.quit()

        camera.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()