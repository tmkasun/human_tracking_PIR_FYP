# Copyright (c) University of Moratuwa


"""
Client program to fetch PIR data from server and analyse the data
"""

from twisted.internet import reactor, protocol
import cv2
import numpy as np
from config import conf


def his_equ(img):
    """
    Histrogram equalization for better contras image
    :param img:
    :return:
    """
    histr = cv2.calcHist([img], [0], None, [256], [0, 256])
    gray_image = np.zeros(img.shape[:2], np.uint8)

    intensity_probability = np.zeros((1, 256))

    row_width = img.shape[:2][0]
    column_width = img.shape[:2][1]
    image_size = row_width * column_width
    # print "Image size = {}".format(image_size)
    alpha = 255 / (image_size)

    for intensity_index in range(len(histr)):
        intensity = histr[intensity_index][0]
        intensity_probability[0][intensity_index] = intensity / image_size

    cumulative_frequency = []
    for intensive_probability_value in intensity_probability[0]:
        if (len(cumulative_frequency) > 0):
            cumulative_frequency.append(cumulative_frequency[-1] + intensive_probability_value)
        else:
            cumulative_frequency.append(intensive_probability_value)

    for value_index in range(len(cumulative_frequency)):
        current_value = cumulative_frequency[value_index]
        scaled_value = current_value * 255
        cumulative_frequency[value_index] = scaled_value

    for row in range(len(img)):
        for column in range(len(img[row])):
            current_value = img[row][column]
            new_value = cumulative_frequency[current_value]
            gray_image[row][column] = new_value

    return gray_image


def draw_histo(img):
    """
    Draw histogram chart for human analysis
    :param img:
    :return:
    """
    histr = cv2.calcHist([img], [0], None, [256], [0, 256])

    max_intensity_value = max(histr)
    min_intensity_value = 0
    new_max = 512
    line_width = 2

    histo_image = np.zeros((new_max, 255 * line_width, 1), np.uint8)

    for intensity_index in range(len(histr)):
        intensity = histr[intensity_index][0]
        normalized_intensity = intensity * (new_max - 0) / (max_intensity_value - 0)
        cv2.line(histo_image, (intensity_index, new_max), (intensity_index, new_max - normalized_intensity),
                 (255, 0, 0), line_width)
    return histo_image


def contrast_stretching(img, r1, r2, s1, s2):
    contrast_image = np.zeros(img.shape[:2], np.uint8)

    for row in range(len(img)):
        for column in range(len(img[row])):
            pixel_value = img[row][column]
            if pixel_value <= r1:
                pixel_value = (s1 / r1) * pixel_value
            elif pixel_value <= r2:
                pixel_value = ((s2 - s1) / (r2 - r1)) * (pixel_value - r1) + s1
            else:
                pixel_value = ((255 - s2) / (255 - r2)) * (pixel_value - r2) + s2

            contrast_image[row][column] = pixel_value

    return contrast_image


class ThermalDataProtocol(protocol.Protocol):
    """Once connected, fetch the thermal data and do analysis """

    def connectionMade(self):
        self.transport.write("ACK")

    def dataReceived(self, data):
        print(data)

        """

        :param data:
        """
        self.transport.write("KeepAlive")

        pixels = data.split(',')  # TODO: string values
        min_temperature = int(min(pixels))
        max_temperature = int(max(pixels))

        # print("Min temp = {}C ({}) ,Max temp = {}C ({})".format(min_temperature * 0.25, min_temperature,
        # max_temperature * 0.25, max_temperature))

        sorted_values = sorted(pixels)
        tenth_max_temperature_value = 132  #int(sorted_values[-10])

        thermal_image = np.zeros((8, 8), dtype=np.uint8)
        enlarge_size = conf.pir['image_size']
        enlarged_thermal_image = np.zeros((enlarge_size, enlarge_size), dtype=np.uint8)
        ratio = enlarge_size / 8

        for row_index in range(8):
            for column_index in range(8):
                thermal_image[row_index][column_index] = int(round(float(pixels[row_index * 8 + column_index])))
                intensity = thermal_image[row_index][column_index]
                corrected_intensity = 255 - intensity  # This is to make hotter values to be appear more darker than cool values
                for rows in range(row_index * ratio, row_index * ratio + ratio):
                    if intensity <= tenth_max_temperature_value:  # If the intensity is less than the tenth maximum temreture value make it white
                        corrected_intensity = 255

                    enlarged_thermal_image[rows][column_index * ratio:column_index * ratio + ratio] = [
                                                                                                          corrected_intensity] * ratio
        # enlarged = np.zeros((128,128),dtype=np.uint8)

        # enlarged =  cv2.resize(thermal_image,(0,0),fx=64,fy=64)

        # cv2.imshow("Thermal snap",thermal_image)
        # cv2.imshow("Thermal_image",enlarged)

        # histogram = draw_histo(enlarged_thermal_image)
        # cv2.imshow("Thermal histro",histogram)

        current_lower = 100
        current_upper = 150

        streched_lower = 10
        streched_upper = 250

        # contrast_stretched = contrast_stretching(enlarged_thermal_image, current_lower, current_upper, streched_lower,streched_upper)
        # cv2.imshow("Contrast_Stretched", contrast_stretched)

        # histro_euqued = his_equ(enlarged_thermal_image)
        # cv2.imshow("Thermal_equalized",histro_euqued)

        cv2.imshow("Raw Image", enlarged_thermal_image)


        # print("Wait for key action")
        # cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            reactor.stop()
        elif cv2.waitKey(1) & 0xFF == ord('i'):
            tenth_max_temperature_value += 1
        elif cv2.waitKey(1) & 0xFF == ord('d'):
            tenth_max_temperature_value -= 1


            # cv2.destroyAllWindows()
            # print("Destroy all opend windows")


            # self.transport.loseConnection()

    def connectionLost(self, reason):
        message_string = "Connection with {} through {} loss due to {} ".format(self.transport.addr[0],
                                                                                self.transport.addr[1], reason.value)
        print(message_string)


class EchoFactory(protocol.ClientFactory):
    protocol = ThermalDataProtocol

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()


# this connects the protocol to a server running on port 8000
def main():
    f = EchoFactory()
    reactor.connectTCP(conf.pir['server'], conf.pir['port'], f)

    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
