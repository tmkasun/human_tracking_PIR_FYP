__author__ = 'tmkasun'
import os
import cv2
import numpy as np


# def deskew(img):
# m = cv2.moments(img)
# if abs(m['mu02']) < 1e-2:
# return img.copy()
# skew = m['mu11'] / m['mu02']
# M = np.float32([[1, skew, -0.5 * SZ * skew], [0, 1, 0]])
# img = cv2.warpAffine(img, M, (SZ, SZ), flags=affine_flags)
# return img

def get_momentum(frame):
    return cv2.moments(frame, binaryImage=False)


bin_n = 16


def hog(frame, return_gx=False):
    gx = cv2.Scharr(frame, cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(frame, cv2.CV_32F, 0, 1)

    magnitude, angle = cv2.cartToPolar(gx, gy)

    quantized_angles = np.int32(bin_n * angle / (2 * np.pi))
    bins = quantized_angles[:10, :10]
    # Quantization into bins
    gx = cv2.convertScaleAbs(gx)
    gy = cv2.convertScaleAbs(gy)

    if return_gx:
        gx = np.absolute(gx)
        return np.uint8(gx)

    return cv2.addWeighted(gx, 0.5, gy, 0.5, 0)

    # cv2.Sobel()
    # cv2.GaussianBlur()


font = cv2.FONT_HERSHEY_PLAIN


def make_comparable(original, manipulated):
    comparison_frame = np.concatenate((original, manipulated), axis=1)
    cv2.putText(comparison_frame, 'Original Frame', (original.shape[1] / 2, 10), font, 0.7, (255, 0, 255), 1,
                cv2.LINE_AA)
    cv2.putText(comparison_frame, 'Manipulated Frame', (original.shape[1] * 3 / 2, 10), font, 0.7, (0, 255, 255), 1,
                cv2.LINE_AA)
    return comparison_frame


def main():
    current_dir = os.path.dirname(__file__)
    sample_file = current_dir + "/../data/sample_data.mov"
    thermal_vid = cv2.VideoCapture(sample_file)
    while thermal_vid.isOpened():
        _, frame = thermal_vid.read()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Get momentum of different order to find centroid and area , shape etc
        # frame_new = get_momentum(frame)

        frame_new = hog(frame_gray)
        # print(frame_new)
        comparison_frame = make_comparable(frame_gray, frame_new)
        cv2.imshow("FLiR Video", comparison_frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()