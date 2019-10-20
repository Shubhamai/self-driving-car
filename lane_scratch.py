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
    
    hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    
    lower_blue = np.array([200,0,0]) 
    upper_blue = np.array([250,250,255])
    
    lower_yellow = np.array([21, 39, 64])
    upper_yellow = np.array([40, 255, 255])
    
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue) # I have the Green threshold image.

    # Threshold the HSV image to get only blue colors
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask = blue_mask + yellow_mask
    # Define the masked area

    #mask = cv2.inRange(result, lower_yellow, upper_yellow)
    res = cv2.bitwise_and(result, result, mask= mask)
    # Vizualize the mask

    
    edges = cv2.Canny(result, 50, 200)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 120, minLineLength=5, maxLineGap=20)
    
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    if lines is None:
        pass
    
    laplacian64 = cv2.Laplacian(res, cv2.CV_64F)
    sobelx64 = cv2.Sobel(res,cv2.CV_64F,1,0,ksize=5)
    sobely64 = cv2.Sobel(res,cv2.CV_64F,0,1,ksize=5)

    laplacian = np.uint8(np.absolute(laplacian64))
    sobelx = np.uint8(np.absolute(sobelx64))
    sobely = np.uint8(np.absolute(sobely64))

    kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, 0]], np.float32) 

    sharpened = cv2.filter2D(result, -1, kernel) # applying the sharpening kernel to the input image & displaying it.
    cv2.imshow('Image Sharpening', sharpened)
    
    cv2.imshow("Perspective transformation", result)
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow("Mask", res)
    cv2.imshow("Sobel Y", sobely)
    cv2.imshow("frame", frame)
    cv2.imshow('Edges', edges)
    cv2.setMouseCallback('frame', mouse_callback)
    
    
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(right_clicks)
