# Importing Libraries
import cv2 
import numpy as np 
import matplotlib.pyplot as plt

# importing the car cascade to detect cats
car_cascade = cv2.CascadeClassifier('cars.xml')

# Making the detect function to detect cars
def detect(gray, frame):

    cars = car_cascade.detectMultiScale(gray, 1.37, 3)
    for (x, y, w, h) in cars:
        cv2.putText(frame, 'car', (x, y), cv2.FONT_ITALIC, 1, (255, 255, 255), 2)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    return frame

# To read the video road.mp4
cap = cv2.VideoCapture('road.mp4')
 
# Read until video is completed
while(cap.isOpened()):

  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur the video
    gray = cv2.blur(gray,(8,8))

    # Detect edges
    edges = cv2.Canny(gray, 50, 200)

    # detect cars
    detected = detect(gray, frame)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 120, minLineLength=5, maxLineGap=20)
    
    # Draw lines on the image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
    if lines is None:
        pass

    cv2.imshow('Frame',frame)
    cv2.imshow('Blur Image', gray)
    cv2.imshow('Edges', edges)
 
    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()