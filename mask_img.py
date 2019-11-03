import cv2

# To make a binary image
def mask_image(frame, white_low, white_high, yellow_low, yellow_high):
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Apply the thresholds to get only white and yellow
    white_mask = cv2.inRange(img_hsv, white_low, white_high)
    yellow_mask = cv2.inRange(img_hsv, yellow_low, yellow_high)

    # Bitwise or the yellow and white mask
    color_mask = cv2.bitwise_or(yellow_mask, white_mask)
    return color_mask
