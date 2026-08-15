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

    # -------- FIND CONTOURS --------
    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # -------- DRAW CONTOURS --------
    contour_view = frame.copy()

    cv2.drawContours(
        contour_view,
        contours,
        -1,
        (0, 255, 0),
        2
    )

    # -------- SHOW WINDOWS --------
    cv2.imshow("Original Frame", frame)

    cv2.imshow("Gray", gray)

    cv2.imshow("Edges", edges)

    cv2.imshow("Contours", contour_view)

    # -------- EXIT --------
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()