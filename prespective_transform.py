import cv2
import numpy as np
import matplotlib.pyplot as plt

# To do prespective transform to the image
def pres_transform(frame, pts1, pts2):

    pts1 = np.float32(pts1)
    pts2 = np.float32(pts2)
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (500, 600))
    return result

# To reverse the prespective transformation
def undo_pres_transform(frame, pts1=np.float32([(0, 0), (1, 0), (0, 1), (1, 1)]), pts2=np.float32([(0.43, 0.65), (0.58, 0.65), (0.1, 1), (1, 1)])):

    frame_size = np.float32([(frame.shape[1], frame.shape[0])])
    pts1 = pts1 * frame_size
    pts2 = pts2 * np.float32([500, 600])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    inverse_pres_transform = cv2.warpPerspective(frame, matrix, (500, 600))
    return inverse_pres_transform

# To draw histogram  of masked image
def draw_hist(frame):
    histogram = np.sum(frame[frame.shape[0]//2:, :], axis=0)
    plt.plot(histogram)
    plt.show()
    return histogram
