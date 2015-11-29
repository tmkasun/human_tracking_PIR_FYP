__author__ = 'tmkasun'

import os
import cv2
from skimage import data, feature
import numpy as np


def skimage_blob(frame):
    gray_frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected_dogs = feature.blob_log(gray_frm)

    for blob in detected_dogs:
        sigma = blob[-1]
        blob_rad = (2 ** 1 / 2) * sigma
        cv2.circle(gray_frm, (blob[1], blob[0]), blob_rad, (255, 0, 0))

    return gray_frm


def opencv_blob(frame):
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 120
    params.maxThreshold = 255

    # # Filter by Area.
    # params.filterByArea = True
    # params.minArea = 15
    #
    # Filter by Circularity
    # params.filterByCircularity = True
    # params.minCircularity = 0.01

    # # Filter by Convexity
    # params.filterByConvexity = True
    # params.minConvexity = 0.4
    #
    # # Filter by Inertia
    params.filterByInertia = True
    params.maxInertiaRatio = 0.7

    detector = cv2.SimpleBlobDetector(params)

    key_points = detector.detect(frame)
    if key_points:
        for key_point in key_points:
            x = int(key_point.pt[0])
            y = int(key_point.pt[1])
            radius = int(key_point.size) * 5
            cv2.circle(frame, (x, y), radius, (0, 0, 255),5)
    # im_with_keypoints = cv2.drawKeypoints(frame, key_points, np.array([]), (0, 0, 255),
    #                                       cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    return frame


def write_to_file(output_video, frame):
    frame = cv2.cvtColor(frame, cv2.cv.CV_GRAY2RGB)
    output_video.write(frame)


def main():
    current_dir = os.path.dirname(__file__)
    sample_file = current_dir + "/../data/sample_data.mov"

    thermal_vid = cv2.VideoCapture(sample_file)
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
    detected_video = cv2.VideoWriter("blob.mp4v", fourcc, 20, (428, 240))

    while thermal_vid.isOpened():
        _, frame = thermal_vid.read()

        im_with_keypoints = opencv_blob(frame)
        # write_to_file(detected_video,im_with_keypoints)
        cv2.imshow("DOG_video", im_with_keypoints)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    thermal_vid.release()
    detected_video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
