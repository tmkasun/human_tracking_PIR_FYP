# coding=utf-8
__author__ = 'tmkasun'
import smbus
from libs.register import Register, AccessMode
from libs.interrupt_handler import InterruptHandler
from libs.thermistor import Thermistor


class GridEye(object):
    PIXEL_DATA_START_REG = 0x80
    PIXEL_DATA_LENGTH = 128
    registers = None
    FPS_1 = 0b1
    FPS_10 = 0b0

    # For some reason continuous i2c reads of 64 bytes and up is causing kernel
    # panic for me (buffer overflow perhaps?). Read 32 bytes at a time.

    def __init__(self, address):

        """
        Pixel Array from 1 to 64 is shown below.

        64 63 62 61 60 59 58￼57
        56 55 54 53 52 51 50 49￼
        48 47￼46￼45 44￼43￼42￼41￼
        40 39 38 37 36 35 34 33
        32 31 30 29 28 27 26 25
        24 23 22 21 20 19 18 17
        16 15 14 13 12 11 10 09
        08 07 06 05 04￼03￼02￼01

        :param address {String} - The address of GridEye sensor in I2C BUS:
        """
        self.address = address
        self.i2c_connection = smbus.SMBus(1)
        self.registers = {
            'PCTL': Register('pctl', 0x00, self),  # Power Control Register
            'RST': Register('rst', 0x01, self, AccessMode.WRITE_ONLY),  # Reset Register Register
            'FPSC': Register('fpsc', 0x02, self),  # Frame Rate Register
            'INTC': Register('intc', 0x03, self),  # Interrupt Control Register
            'STAT': Register('stat', 0x04, self, AccessMode.READ_ONLY),  # Status Register
            'SCLR': Register('sclr', 0x05, self),  # Status Clear Register
            'AVE': Register('ave', 0x06, self),  # Average Register
            'INTR': InterruptHandler(self),  # Interrupt Level Register #TODO: Not implemented yet
            'THM': Thermistor(self),  # Thermistor Register
        }

    @property
    def pctl(self):
        return self.registers['pcrl'][1]

    @property
    def thermistor_value(self):
        thermistor = self.registers['THM']
        return thermistor.get_temperature()

    @property
    def frame_rate(self):
        return self.registers['FPSC'].value

    @frame_rate.setter
    def frame_rate(self, value):
        if value not in [self.FPS_1, self.FPS_10]:
            raise Exception(
                "Incorrect frame rate: {}, Frame rate should be GridEye.FPS_1 or GridEye.FPS_10".format(value))
        self.registers['FPSC'].value = value

    def get_frame(self):
        """ Retrieves and returns a frame(In the image processing perspective) of temperature data from the sensor. """
        frame = []
        tx_string = ""
        for i in range(0, 128, 2):
            # value = registers[i + 1] << 8 | registers[i]
            value = (self.i2c_connection.read_byte_data(self.address, self.PIXEL_DATA_START_REG + (
                i + 1)) << 8 | self.i2c_connection.read_byte_data(self.address, self.PIXEL_DATA_START_REG + i))

            if value & (0x1 << 11):
                # do 2's compliment conversion
                value -= 2048

            # value *= 0.25  # convert to C
            frame.append(value)
            tx_string += str(value) + ','

        return tx_string[:-1]  # Remove the last comma

