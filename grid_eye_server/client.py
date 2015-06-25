# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


"""
An example client. Run simpleserv.py first before running this.
"""

from twisted.internet import reactor, protocol
import cv2
import numpy as np





def his_equ(img):
    print("Generating histrogram equlization")
    histr = cv2.calcHist([img],[0],None,[256],[0,256])
    gray_image = np.zeros(img.shape[:2],np.uint8)

    intensity_probability = np.zeros((1,256))

    row_width = img.shape[:2][0]
    column_width = img.shape[:2][1]
    image_size = row_width*column_width
    print "Image size = {}".format(image_size)
    alpha = 255/(image_size)

    for intensity_index in range(len(histr)):
        intensity = histr[intensity_index][0]
        intensity_probability[0][intensity_index] =  intensity/image_size

    cumulative_frequency = []
    for intensive_probability_value in intensity_probability[0]:
        if(len(cumulative_frequency)>0):
            cumulative_frequency.append(cumulative_frequency[-1]+intensive_probability_value)
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
    print("Drawing histogram....")
    histr = cv2.calcHist([img],[0],None,[256],[0,256])

    max_intensity_value = max(histr)
    min_intensity_value = 0
    new_max = 512
    line_width = 2

    histo_image = np.zeros((new_max,255*line_width,1),np.uint8)

    for intensity_index in range(len(histr)):
        intensity = histr[intensity_index][0]
        normalized_intensity = intensity*(new_max-0)/(max_intensity_value-0)
        cv2.line(histo_image,(intensity_index,new_max),(intensity_index,new_max-normalized_intensity),(255,0,0),line_width)
    return histo_image


# a client protocol

class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
        self.transport.write("hello, world!")

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "Server said:", data

        self.transport.write("Loop")


        pixels = data.split(',') # TODO: string values
        thermal_image = np.zeros((8,8),dtype=np.uint8)

        for row_index in range(8):
            for column_index in range(8):
                thermal_image[row_index][column_index] = int(round(float(pixels[row_index*8 + column_index])))


        # enlarged = np.zeros((128,128),dtype=np.uint8)

        enlarged =  cv2.resize(thermal_image,(0,0),fx=64,fy=64)

        # cv2.imshow("Thermal snap",thermal_image)
        cv2.imshow("Thermal_image",enlarged)

        # histogram = draw_histo(thermal_image)
        # cv2.imshow("Thermal histro",histogram)


        histro_euqued = his_equ(enlarged)
        cv2.imshow("Thermal_equalized",histro_euqued)


        # print("Wait for key action")
        cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print("Destroy all opend windows")


        # self.transport.loseConnection()

    def connectionLost(self, reason):
        print "connection lost"


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()



# this connects the protocol to a server running on port 8000
def main():
    f = EchoFactory()
    reactor.connectTCP("192.168.1.1", 8000, f)

    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
