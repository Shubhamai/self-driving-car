# Importing Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

cap = cv2.VideoCapture('road.mp4')

from mouse_call import mouse_callback
from mask_img import mask_img
from prespective_transform import pres_transform
from edge_detect import detect_edges
from camera_calib import do_calibration, undistort
from config import *


# Read until video is completed
while(cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    
    undistorted_frame = undistort(mtx, dist, frame)
    
    result = pres_transform(pts1, pts2, frame)
    edges = detect_edges(result)
    
    
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

    Vizualize the mask

        
    masked_image = mask_img(frame)
    cv2.imshow('Mask_img', masked_image)
    cv2.imshow('undistort_image', undistorted_frame)
    cv2.imshow("Perspective transformation", result)

    cv2.imshow("Mask", color_mask)
    cv2.imshow('Edges', edges)
    cv2.setMouseCallback('frame', mouse_callback)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

