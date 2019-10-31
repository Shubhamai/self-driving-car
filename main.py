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

cap = cv2.VideoCapture('road.mp4')


# Read until video is completed
while(cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()

    undistorted_frame = undistort(mtx, dist, frame)

    cropped_image = crop_img(undistorted_frame)

    result = pres_transform(undistorted_frame, pts1, pts2)

    edges = detect_edges(result, canny_threshold1, canny_threshold2, hough_rho,
                         hough_theta, hough_threshold, hough_lines, hough_minLineLength, hough_maxLineGap)

    color_mask = mask_image(
        result, white_low, white_high, yellow_low, yellow_high)

    undo_pres = undo_pres_transform(result)
    
    one, two = crop_img_two(color_mask)
    
    # draw_hist(color_mask)

    cv2.imshow('crop_img', cropped_image)
    cv2.imshow('undistort_image', undistorted_frame)
    cv2.imshow("Perspective transformation", result)
    cv2.imshow("Mask", color_mask)
    cv2.imshow('undo', undo_pres)
    cv2.imshow('frame', frame)
    cv2.imshow('one', one)
    cv2.imshow('two', two)
    cv2.imshow('Edges', edges)
    cv2.setMouseCallback('Mask', mouse_callback)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
