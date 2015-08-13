__author__ = 'tmkasun'
from register import Register, AccessMode


class Thermistor(object):
    POSITIVE_SIGN = 0b0000
    NEGATIVE_SIGN = 0b1000
    TEMPERATURE_RESOLUTION = 0.0625

    def __init__(self, device):
        self.tthl = Register('TTHL', 0x0E, device, AccessMode.READ_ONLY)
        self.tthh = Register('TTHH', 0x0F, device, AccessMode.READ_ONLY)
        self._device = device

    def get_temperature(self):
        tthl_value = self.tthl.value
        tthh_value = self.tthh.value

        sign_filter = 0b00001000
        sign = tthh_value & sign_filter

        data_filter = 0b00000111
        higher_data = tthh_value & 0b00000111

        shifted_highr_data = higher_data << 8
        thermal_data_12bits = shifted_highr_data | tthl_value
        temperature = thermal_data_12bits * self.TEMPERATURE_RESOLUTION
        return temperature