# Importing Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt

cap = cv2.VideoCapture('road.mp4')

right_clicks = list()

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):

    #right-click event value is 2
    if event == 2:
        global right_clicks

        #store the coordinates of the right-click event
        right_clicks.append([x, y])

        #this just verifies that the mouse data is being collected
        #you probably want to remove this later
        print(right_clicks)
        

# Read until video is completed
while(cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    mask = np.zeros(frame.shape, dtype=np.uint8)
    roi_corners = np.array([[(651, 371), (174, 686), (1226, 656)]], dtype=np.int32)
    white = (255, 255, 255)
    cv2.fillPoly(mask, roi_corners, white)

    # apply the mask
    masked_image = cv2.bitwise_and(frame, mask)


    #shrink the top
    iii = 0
    #the matrix sum of back is 0
    while  not np.sum(masked_image[iii,:,:]):
            resized_top = masked_image[iii+1:,:,:]
            iii = iii + 1


    #shrink the bottom
    size_img = resized_top.shape
    iii = size_img[0]
    while not np.sum(resized_top[iii-2:iii-1,:,:]):
            resized_bottom = resized_top[0:iii-1,:,:]
            iii = iii - 1

    #shrink the left
    iii = 0
    while  not np.sum(resized_bottom[:,iii,:]):
            resized_left = resized_bottom[:,iii+1:,:]
            iii = iii + 1

    #shrink the right
    size_img = resized_left.shape
    iii = size_img[1]

    while  not np.sum(resized_left[:,iii-2:iii-1,:]):
            resized_right = resized_left[:,0:iii-1:,:]
            iii = iii - 1


    
    pts1 = np.float32([[476, 478], [757, 454], [108, 639], [1174, 621]])
    pts2 = np.float32([[0, 0], [500, 0], [0, 600], [500, 600]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (500, 600))
    cv2.imshow("Perspective transformation", result)


    #display your handywork
    cv2.imshow('masked image', resized_right)
    
    cv2.setMouseCallback('image', mouse_callback)
    cv2.imshow("frame", frame)
    cv2.setMouseCallback('frame', mouse_callback)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(right_clicks)