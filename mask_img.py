import numpy as np
import cv2


def mask_img(frame):

    mask = np.zeros(frame.shape, dtype=np.uint8)

    roi_corners = np.array(
        [[(651, 371), (174, 686), (1226, 656)]], dtype=np.int32)
    white = (255, 255, 255)
    cv2.fillPoly(mask, roi_corners, white)

    # apply the mask
    masked_image = cv2.bitwise_and(frame, mask)

    # shrink the top
    iii = 0
    # the matrix sum of back is 0
    while not np.sum(masked_image[iii, :, :]):
        resized_top = masked_image[iii+1:, :, :]
        iii = iii + 1

    # shrink the bottom
    size_img = resized_top.shape
    iii = size_img[0]
    while not np.sum(resized_top[iii-2:iii-1, :, :]):
        resized_bottom = resized_top[0:iii-1, :, :]
        iii = iii - 1

    # shrink the left
    iii = 0
    while not np.sum(resized_bottom[:, iii, :]):
        resized_left = resized_bottom[:, iii+1:, :]
        iii = iii + 1

    # shrink the right
    size_img = resized_left.shape
    iii = size_img[1]

    while not np.sum(resized_left[:, iii-2:iii-1, :]):
        resized_right = resized_left[:, 0:iii-1:, :]
        iii = iii - 1

    return resized_right
