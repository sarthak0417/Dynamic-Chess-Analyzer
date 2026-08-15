import chess
import chess.engine

from src.config import STOCKFISH_PATH


def start_engine():
    engine = chess.engine.SimpleEngine.popen_uci(
        STOCKFISH_PATH
    )

    return engine


def analyze_position(
    engine,
    board,
    depth=15,
    perspective=None
):
    result = engine.analyse(
        board,
        chess.engine.Limit(depth=depth)
    )

    if perspective is None:
        perspective = board.turn

    best_move = None

    if "pv" in result and result["pv"]:
        best_move = result["pv"][0]

    score = result["score"].pov(
        perspective
    )

    return {
        "best_move": best_move,
        "score": score,
        "depth": result.get("depth", depth),
    }


def score_to_centipawns(score):
    value = score.score(
        mate_score=100000
    )

    if value is None:
        return 0

    return value