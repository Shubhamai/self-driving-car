import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import pickle

def do_calibration():
    #for camera calibration and store the result in a file "camera_cal/camera_cal.p" 
    #Array to store the obj point and image points
    objpoints = []
    imgpoints = []
    objp = np.zeros((6*9,3),np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    images = glob.glob("chessboard images/cal*")
    for fnames in images:
        img = mpimg.imread(fnames)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,6), None)
        if ret == True:
            imgpoints.append(corners)
            objpoints.append(objp)
            #draw lines on the cheesboard
            img = cv2.drawChessboardCorners(img, (9,6), corners, ret)
            #plt.imshow(img)
    img_size = mpimg.imread("chessboard images/calibration1.jpg")
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    #save the calibration data in a pickle file to use later
    camera_cal_val = "camera_cal/camera_cal.p" 
    output = open(camera_cal_val, 'wb')

    mydict2 = {'mtx': 1, 'dist': 2}
    mydict2['mtx'] = mtx
    mydict2['dist'] = dist
    pickle.dump(mydict2, output)
    output.close()

def get_camera_calibration():
    dist_pickle = pickle.load( open( "camera_cal/camera_cal.p", "rb" ) )
    mtx = dist_pickle["mtx"]
    dist = dist_pickle["dist"]
    return mtx, dist
    
#do_calibration()
mtx, dist = get_camera_calibration()
print(f"mtx : {mtx} distance : {dist}")