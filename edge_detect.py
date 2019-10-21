import cv2
import numpy as np

def detect_edges(frame):

    edges = cv2.Canny(frame, 50, 200)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 120,
                            minLineLength=5, maxLineGap=20)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    if lines is None:
        pass

    return edges
