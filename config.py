from camera_calib import do_calibration

# Prespective transform
pts1 = [[522, 474], [733, 463], [202, 664], [1197, 635]]
pts2 = [[0, 0], [500, 0], [0, 600], [500, 600]]

# Camera calibration
mtx, dist = do_calibration('chessboard images', 'calibration', 9, 6, (720, 1280))

