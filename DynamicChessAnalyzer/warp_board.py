import cv2
import numpy as np


def order_points(points):
    points = points.reshape((4, 2)).astype("float32")

    rect = np.zeros((4, 2), dtype="float32")

    s = points.sum(axis=1)
    diff = np.diff(points, axis=1)

    rect[0] = points[np.argmin(s)]       # top-left
    rect[1] = points[np.argmin(diff)]    # top-right
    rect[2] = points[np.argmax(s)]       # bottom-right
    rect[3] = points[np.argmax(diff)]    # bottom-left

    return rect


def warp_board(image, contour, size=800):
    pts1 = order_points(contour)

    pts2 = np.float32([
        [0, 0],
        [size, 0],
        [size, size],
        [0, size]
    ])

    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    warped = cv2.warpPerspective(image, matrix, (size, size))

    return warped