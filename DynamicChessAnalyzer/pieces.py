import cv2
import numpy as np

def detect_piece(square):

    # Convert to grayscale
    gray = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)

    # Reduce noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold image
    _, thresh = cv2.threshold(
        blur,
        100,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Count white pixels
    white_pixels = cv2.countNonZero(thresh)

    # Detect piece
    if white_pixels > 500:
        return "piece"
    else:
        return "empty"