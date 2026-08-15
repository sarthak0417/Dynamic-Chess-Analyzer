import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Flip webcam
    frame = cv2.flip(frame, 1)

    # -------- PREPROCESS --------
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)

    cv2.imshow("Edges", edges)

    # -------- FIND CONTOURS --------
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    max_area = 0
    best_contour = None

    for cnt in contours:

        area = cv2.contourArea(cnt)

        # Ignore small contours
        if area > 10000:

            peri = cv2.arcLength(cnt, True)

            approx = cv2.approxPolyDP(
                cnt,
                0.02 * peri,
                True
            )

            # Only 4-corner contours
            if len(approx) == 4:

                if area > max_area:
                    max_area = area
                    best_contour = approx

    # -------- DRAW DETECTED BOARD --------
    board_view = frame.copy()

    if best_contour is not None:

        cv2.drawContours(
            board_view,
            [best_contour],
            -1,
            (0, 255, 0),
            4
        )

        cv2.putText(
            board_view,
            "Chessboard Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            board_view,
            "Board Not Detected",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    # -------- SHOW RESULT --------
    cv2.imshow("Detected Board", board_view)

    # -------- EXIT --------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()