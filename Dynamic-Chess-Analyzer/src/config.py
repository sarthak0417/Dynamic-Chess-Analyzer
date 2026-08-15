import os
from pathlib import Path

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_DIR / ".env")

stockfish_path = os.getenv("STOCKFISH_PATH")

if not stockfish_path:
    raise RuntimeError(
        "STOCKFISH_PATH is missing from the .env file."
    )

stockfish_path = Path(stockfish_path)

if not stockfish_path.is_absolute():
    stockfish_path = ROOT_DIR / stockfish_path

STOCKFISH_PATH = str(stockfish_path.resolve())

BOARD_SIZE = 800
GRID_SIZE = 8
SQUARE_SIZE = BOARD_SIZE // GRID_SIZE

CAMERA_INDEX = 0

DIFF_THRESHOLD = 18.0