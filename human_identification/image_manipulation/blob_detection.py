__author__ = 'tmkasun'

import os
import cv2
from skimage import data, feature
import numpy as np
from datetime import datetime


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
            cv2.circle(frame, (x, y), radius, (0, 0, 255), 5)

    return frame


class VideoWriter(object):
    def __init__(self, shape, type='mp4v', frame_rate=20, is_color=False):
        self.fourcc = cv2.VideoWriter_fourcc(*type)
        timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M")
        output_file = "output_video_{}.mp4v".format(timestamp)
        self.output_video = cv2.VideoWriter(output_file, self.fourcc, frame_rate, shape)

    def write(self, frame):
        # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        self.output_video.write(frame)


fgbg_knn = cv2.createBackgroundSubtractorKNN()
fgbg_mog2 = cv2.createBackgroundSubtractorMOG2(detectShadows=False, varThreshold=100, history=500)
# fgbg_gmg = cv2.BackgroundSubtractorGMG()
def backgroud_substraction(frame, method='MOG2'):
    """
    Rerun foreground mask subtracting the background from the given frame according to the method specified
    :param frame:
    :param method:
    :return:
    Supported methods: MOG(Mixture of Gaussian),
    """
    if method == "MOG":
        pass
        # foreground_mask = fgbg2.apply(frame)
    elif method == "MOG2":
        foreground_mask = fgbg_mog2.apply(frame)
    elif method == "KNN":
        foreground_mask = fgbg_knn.apply(frame)

    return foreground_mask


def draw_contours(frame):
    imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    font = cv2.FONT_HERSHEY_PLAIN

    min_human_body_width = 20  # TODO: This is so dum change this , no logical reason at all
    max_human_body_width = 100  # TODO: This is so dum change this , no logical reason at all
    detected_object = 0  # TODO: This is so dum change this , no logical reason at all
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if max_human_body_width > w > min_human_body_width:
            detected_object += 1
            contour_image = cv2.drawContours(frame, [contour], 0, (12, 20, 255), 2)
            contour_bounded_rect = cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Object ID : {}'.format(detected_object), (x + w, y + h), font, 0.7, (255, 255, 255), 1,
                        cv2.LINE_AA)
        else:
            contour_bounded_rect = frame

    cv2.putText(frame, 'Number of objects: {}'.format(detected_object), (5, 15), font, 0.7, (255, 255, 255), 1,
                cv2.LINE_AA)

    return contour_bounded_rect


def main():
    current_dir = os.path.dirname(__file__)
    sample_file = current_dir + "/../data/sample_data.mov"

    thermal_vid = cv2.VideoCapture(sample_file)
    video_output = VideoWriter((428, 240))
    while thermal_vid.isOpened():
        _, frame = thermal_vid.read()

        # filtered_frame = opencv_blob(frame)
        # filtered_frame = backgroud_substraction(frame)
        filtered_frame = draw_contours(frame)

        # video_output.write(filtered_frame)
        cv2.imshow("filtered_frame", filtered_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    thermal_vid.release()
    video_output.output_video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
