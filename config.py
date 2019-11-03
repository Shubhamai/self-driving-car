from camera_calib import do_calibration
import numpy as np

# Prespective transform
pts1 = [[521, 480], [764, 474], [215, 646], [1190, 640]]
pts2 = [[0, 0], [500, 0], [0, 600], [500, 600]]

# Camera calibration
mtx, dist = do_calibration(
    'chessboard images', 'calibration', 9, 6, (720, 1280))

# Edge Detector
canny_threshold1 = 50
canny_threshold2 = 200
hough_rho = 1
hough_theta = np.pi/180
hough_threshold = 120
hough_lines = None
hough_minLineLength = 5
hough_maxLineGap = 20

# Image Mask
white_low = np.array([0, 0, 210])
white_high = np.array([255, 30, 255])

yellow_low = np.array([0, 50, 0])
yellow_high = np.array([110, 255, 255])

# Crop Image in two parts
left_shape = [[0, 600], [0, 250]]
right_shape = [[0, 600], [250, 500]]
