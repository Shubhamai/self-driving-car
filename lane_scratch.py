# Importing Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

cap = cv2.VideoCapture('road.mp4')

from mouse_call import mouse_callback
from crop import crop_img
from prespective_transform import pres_transform
from edge_detect import detect_edges
from camera_calib import do_calibration, undistort
from mask_img import mask_image
from config import *


# Read until video is completed
while(cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
    
    undistorted_frame = undistort(mtx, dist, frame)
    
    cropped_image = crop_img(undistorted_frame)
    
    result = pres_transform(pts1, pts2, undistorted_frame)
    
    edges = detect_edges(result, canny_threshold1, canny_threshold2, hough_rho, hough_theta , hough_threshold, hough_lines , hough_minLineLength, hough_maxLineGap)
    
    color_mask = mask_image(result, white_low, white_high, yellow_low, yellow_low)
    
    
    cv2.imshow('crop_img', cropped_image)
    cv2.imshow('undistort_image', undistorted_frame)
    cv2.imshow("Perspective transformation", result)
    cv2.imshow("Mask", color_mask)
    cv2.imshow('frame', frame)
    cv2.imshow('Edges', edges)
    cv2.setMouseCallback('frame', mouse_callback)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

