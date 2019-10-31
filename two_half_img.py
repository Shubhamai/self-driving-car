import numpy as np
import cv2

def crop_img_two(frame):
    MARGIN = 10
    hist = np.sum(frame, axis=0)
    lhist, rhist = hist[:262], hist[262:]
    lcenter, rcenter = np.argmax(lhist), np.argmax(rhist)+262
    llo, lhi, rlo, rhi = lcenter-MARGIN, lcenter+MARGIN, rcenter-MARGIN, rcenter+MARGIN
    return frame[:,llo:lhi], frame[:,rlo:rhi]