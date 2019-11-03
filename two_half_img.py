import numpy as np
import cv2


def crop_img_two(frame, one_shape, two_shape):
    left_line = frame[one_shape[0][0]:one_shape[0]
                [1], one_shape[1][0]:one_shape[1][1]]
    right_line = frame[two_shape[0][0]:two_shape[0]
                [1], two_shape[1][0]:two_shape[1][1]]
    return left_line, right_line
