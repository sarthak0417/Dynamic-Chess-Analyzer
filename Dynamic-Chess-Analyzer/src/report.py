import json
from datetime import datetime
from pathlib import Path

import chess
import chess.pgn

from src.config import ROOT_DIR


REPORT_DIRECTORY = (
    ROOT_DIR / "reports"
)


def create_pgn(board):
    game = chess.pgn.Game()

    game.headers[
        "Event"
    ] = "Dynamic Chess Analyzer"

    game.headers[
        "Date"
    ] = datetime.now().strftime(
        "%Y.%m.%d"
    )

    game.headers[
        "Result"
    ] = (
        board.result()
        if board.is_game_over()
        else "*"
    )

    node = game

    replay_board = chess.Board()

    for move in board.move_stack:
        node = node.add_variation(
            move
        )

        replay_board.push(move)

    return game


def save_game_report(
    history,
    board
):
    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    json_path = (
        REPORT_DIRECTORY /
        f"analysis_{timestamp}.json"
    )

    pgn_path = (
        REPORT_DIRECTORY /
        f"game_{timestamp}.pgn"
    )

    report = {
        "result": (
            board.result()
            if board.is_game_over()
            else "*"
        ),
        "total_moves": len(history),
        "moves": history,
    }

    with open(
        json_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )

    game = create_pgn(
        board
    )

    with open(
        pgn_path,
        "w",
        encoding="utf-8"
    ) as file:

        print(
            game,
            file=file
        )

    return json_path, pgn_path