# Importing Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('road.mp4')

right_clicks = list()

# this function will be called whenever the mouse is right-clicked


def mouse_callback(event, x, y, flags, params):

    # right-click event value is 2
    if event == 2:
        global right_clicks

        # store the coordinates of the right-click event
        right_clicks.append([x, y])

        # this just verifies that the mouse data is being collected
        # you probably want to remove this later
        print(right_clicks)


# Read until video is completed
while(cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
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

    pts1 = np.float32([[522, 474], [733, 463], [202, 664], [1197, 635]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (500, 600))

    img_hsv = cv2.cvtColor(result, cv2.COLOR_RGB2HSV)

    # Define color thresholds in HSV
    white_low = np.array([[[0, 0, 210]]])
    white_high = np.array([[[255, 30, 255]]])

    yellow_low = np.array([[[18, 80, 80]]])
    yellow_high = np.array([[[30, 255, 255]]])

    # Apply the thresholds to get only white and yellow
    white_mask = cv2.inRange(img_hsv, white_low, white_high)
    yellow_mask = cv2.inRange(img_hsv, yellow_low, yellow_high)

    # Bitwise or the yellow and white mask
    color_mask = cv2.bitwise_or(yellow_mask, white_mask)

    # Vizualize the mask

    edges = cv2.Canny(result, 50, 200)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 120,
                            minLineLength=5, maxLineGap=20)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    if lines is None:
        pass

    cv2.imshow("Perspective transformation", result)
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow("Mask", color_mask)

    cv2.imshow("frame", frame)
    cv2.imshow('Edges', edges)
    cv2.setMouseCallback('frame', mouse_callback)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(right_clicks)
