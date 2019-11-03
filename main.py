# Importing Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

# Importing custom Libraries
from config import *
from mask_img import mask_image
from camera_calib import do_calibration, undistort
from edge_detect import detect_edges
from prespective_transform import pres_transform, undo_pres_transform, draw_hist
from crop import crop_img
from mouse_call import mouse_callback
from two_half_img import crop_img_two

# Reading video
cap = cv2.VideoCapture('road.mp4')

# Read until video is completed
while(cap.isOpened()):

    # Capture frame-by-frame
    _, frame = cap.read()

    # Undistort the frame
    undistorted_frame = undistort(mtx, dist, frame)

    # Crop the frame
    cropped_image = crop_img(undistorted_frame)

    # Prespective transform the frame
    result = pres_transform(undistorted_frame, pts1, pts2)

    # Binary frame
    color_mask = mask_image(
        result, white_low, white_high, yellow_low, yellow_high)

    # Undo the prespective transfrom
    undo_pres = undo_pres_transform(result)

    # Crop the prespective transform frame into two halves
    left_line, right_line = crop_img_two(color_mask, left_shape, right_shape)
    
    # Detect edges from the prespective trainsform frame
    edges, x, y = detect_edges(left_line, canny_threshold1, canny_threshold2,                                      hough_rho,hough_theta, hough_threshold,                                             hough_lines, hough_minLineLength,                                                   hough_maxLineGap)
    print(f'x = {x}')
    print('-'*56)
    print(f'y = {y}')
    
    # Draw histogram of the binary image
    #histogram = draw_hist(left_line)
    
    
    cv2.imshow('crop_img', cropped_image)
    cv2.imshow('undistort_image', undistorted_frame)
    cv2.imshow("Perspective transformation", result)
    cv2.imshow("Mask", color_mask)
    cv2.imshow('undo', undo_pres)
    cv2.imshow('frame', frame)    
    cv2.imshow('Left Lane', left_line)
    cv2.imshow('Right Lane', right_line)
    cv2.imshow('Edges', edges)
    cv2.setMouseCallback('Mask', mouse_callback)

    # Break the loop when when Q key is pressed
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
