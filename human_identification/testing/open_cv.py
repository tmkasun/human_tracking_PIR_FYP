__author__ = 'tmkasun'

import cv2

import numpy as np


sample_flir = np.random.random_integers(180, 255, size=(80, 60))
print(sample_flir)
cv2.imshow("FLiR Sample image", sample_flir)
cv2.waitKey(0)