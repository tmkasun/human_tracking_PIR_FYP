from cv2.cv import CV_INTER_LINEAR

__author__ = 'tmkasun'

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = frame
    r = 500.0 / gray.shape[1]
    dim = (500, int(gray.shape[0] * r))
    resized_frame = cv2.resize(gray, dim,interpolation=CV_INTER_LINEAR)
    # Display the resulting frame
    cv2.imshow('frame', resized_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()