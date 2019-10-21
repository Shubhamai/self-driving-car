import cv2
import numpy as np


def pres_transform(pts1, pts2, frame):

    pts1 = np.float32(pts1)
    pts2 = np.float32(pts2)
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (500, 600))
    return result
