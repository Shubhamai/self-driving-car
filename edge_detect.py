import cv2
import numpy as np


def detect_edges(frame, canny_threshold1, canny_threshold2, hough_rho, hough_theta, hough_threshold, hough_lines=None, hough_minLineLength=None, hough_maxLineGap=None):

    edges = cv2.Canny(frame, canny_threshold1, canny_threshold2)

    lines = cv2.HoughLinesP(edges, hough_rho, hough_theta, hough_threshold,
                            minLineLength=hough_minLineLength, maxLineGap=hough_maxLineGap)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    if lines is None:
        pass

    return edges
