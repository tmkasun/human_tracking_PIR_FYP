__author__ = 'tmkasun'

import os
import cv2
from skimage import data, feature
import numpy as np
from datetime import datetime
from config import parameters

from socket import socket, AF_INET, SOCK_STREAM
import json
from config.parameters import configs

serverHost = configs['host']
serverPort = configs['service_port']

sSock = socket(AF_INET, SOCK_STREAM)
sSock.connect((serverHost, serverPort))


def send_position(coordinates):
    sSock.send(json.dumps(coordinates))
    # data = sSock.recv(1024)


def skimage_blob(frame):
    # gray_frm = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected_dogs = feature.blob_log(frame)

    for blob in detected_dogs:
        sigma = blob[-1]
        blob_rad = (2 ** 1 / 2) * sigma
        cv2.circle(frame, (blob[1], blob[0]), blob_rad, (255, 0, 0))

    return frame


def opencv_blob(frame):
    # Setup SimpleBlobDetector parameters.
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

    detector = cv2.SimpleBlobDetector_create(params)

    key_points = detector.detect(frame)
    if key_points:
        for key_point in key_points:
            x = int(key_point.pt[0])
            y = int(key_point.pt[1])
            radius = int(key_point.size) * 5
            cv2.circle(frame, (x, y), radius, (0, 0, 255), 5)

    return frame


def image_writer(image):
    timestamp = datetime.now().strftime("%d__%H_%M_%s")
    output_file = parameters.configs['data_directory'] + "/img/image_output_{}.jpg".format(timestamp)
    cv2.imwrite(output_file, image)


class VideoWriter(object):
    def __init__(self, shape, type='mp4v', frame_rate=20, is_color=False):
        self.fourcc = cv2.VideoWriter_fourcc(*type)
        timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M")
        output_file = parameters.configs['data_directory'] + "/vid/output_video_{}.mp4v".format(timestamp)
        self.output_video = cv2.VideoWriter(output_file, self.fourcc, frame_rate, shape)

    def write(self, frame):
        # frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
        self.output_video.write(frame)


fgbg_knn = cv2.createBackgroundSubtractorKNN()
fgbg_mog2 = cv2.createBackgroundSubtractorMOG2(detectShadows=True, varThreshold=50, history=500)
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


def draw_contours(frame, filtered_frame):
    ret, thresh = cv2.threshold(filtered_frame, 100, 255, 0)
    image, contours, hierarchies = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    font = cv2.FONT_HERSHEY_PLAIN

    min_human_body_width = 50  # TODO: This is so dum change this , no logical reason at all
    max_human_body_width = 150  # TODO: This is so dum change this , no logical reason at all
    detected_objects = []
    contour_bounded_rect = None
    try:
        hierarchies = hierarchies[0]
    except TypeError:
        hierarchies = []

    for contour, hierarchy in zip(contours, hierarchies):
        _, _, _, parent_contour_index = hierarchy
        if parent_contour_index >= 0:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        if max_human_body_width > w > min_human_body_width or max_human_body_width > h > min_human_body_width:
            # fixed_w_h = h = w = 100
            # image_writer(frame[y:y + h, x:x + w])
            center_x = (x + (x + w)) / 2.0
            center_y = (y + (y + h)) / 2.0
            centroid = (center_y, center_x)
            detected_objects.append(centroid)
            contour_image = cv2.drawContours(frame, [contour], 0, (12, 20, 255), 2)
            contour_bounded_rect = cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(contour_bounded_rect, 'Object ID : {}'.format(detected_objects), (x + w, y + h), font, 0.7,
                        (255, 255, 255), 1,
                        cv2.LINE_AA)
        else:
            contour_bounded_rect = frame

    total_humans = len(detected_objects)
    if total_humans > 0:
        send_position(detected_objects)
    cv2.putText(frame, 'Number of objects: {}'.format(total_humans), (5, 15), font, 0.7, (255, 255, 255), 1,
                cv2.LINE_AA)

    if contour_bounded_rect is not None:
        return contour_bounded_rect
    else:
        return frame


font = cv2.FONT_HERSHEY_PLAIN


def make_comparable(original, manipulated):
    comparison_frame = np.concatenate((original, manipulated), axis=1)
    cv2.putText(comparison_frame, 'Original Frame', (original.shape[1] / 2, 10), font, 0.7, (255, 0, 255), 1,
                cv2.LINE_AA)
    cv2.putText(comparison_frame, 'Manipulated Frame', (original.shape[1] * 3 / 2, 10), font, 0.7, (0, 255, 255), 1,
                cv2.LINE_AA)
    return comparison_frame


def main():
    path_to_sample = parameters.configs['data_directory'] + "normal_cam_sample_with_back3.mov"

    thermal_vid = cv2.VideoCapture(path_to_sample)
    video_output = VideoWriter((428, 240))
    number_of_frames = thermal_vid.get(cv2.CAP_PROP_FRAME_COUNT)
    print("Total frame cont:{}".format(number_of_frames))
    while thermal_vid.isOpened():
        _, frame_rgb = thermal_vid.read()

        frame_gry = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)
        filtered_frame = backgroud_substraction(frame_gry)
        # filtered_frame = opencv_blob(frame_gry)
        filtered_frame = draw_contours(frame_rgb.copy(), filtered_frame)

        # video_output.write(filtered_frame)
        comparison_frame = make_comparable(frame_rgb, filtered_frame)

        cv2.imshow("filtered_frame", comparison_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    sSock.shutdown(0)
    sSock.close()

    thermal_vid.release()
    video_output.output_video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
