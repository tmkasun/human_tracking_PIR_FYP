__author__ = 'tmkasun'

import smbus
import threading
from twisted.internet import reactor, protocol

class GridEye(object):
    PIXEL_DATA_START_REG = 0x80
    PIXEL_DATA_LENGTH = 128
    # For some reason contiuous i2c reads of 64 bytes and up is causing kernel
    # panic for me (buffer overflow perhaps?). Read 32 bytes at a time.

    def __init__(self, address):

        self.address = address
        self.i2c_connection = smbus.SMBus(1)

    def get_frame(self):
        """ Retrieves and returns a frame of temperature data from the sensor. """
        frame = []
        tx_string = ""
        for i in range(0, 128, 2):
            # value = registers[i + 1] << 8 | registers[i]
            value = (self.i2c_connection.read_byte_data(self.address, self.PIXEL_DATA_START_REG + (
                i + 1)) << 8 | self.i2c_connection.read_byte_data(self.address, self.PIXEL_DATA_START_REG + i))

            if value & (0x1 << 11):
                # do 2's compliment conversion
                value = value - 2048

            # value *= 0.25  # convert to C
            frame.append(value)
            tx_string += str(value) + ','
            # print(value)

        # return frame
        return tx_string[:-1]  # Remove the last comma



class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        # print("Received request from")
        tx_data = sensor.get_frame()
        self.transport.write(tx_data)


def main():
    global sensor
    sensor = GridEye(0x68)
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000,factory)
    print("Server sarted on port 8080")
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()