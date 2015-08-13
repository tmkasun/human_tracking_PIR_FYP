__author__ = 'tmkasun'

import smbus


class AccessMode(object):
    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_WRITE = 3


class Register(object):
    def __init__(self, name, address, device, rw_mode=AccessMode.READ_WRITE):
        self._name = name
        self._address = address
        self._value = None
        self.access_mode = rw_mode
        self.device = device
        self._i2c_connection = smbus.SMBus(1)


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise Exception("Can't set name after initializing")


    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        raise Exception("Can't set address after initializing")

    @property
    def value(self):
        current_value = self._i2c_connection.read_byte_data(self.device.address, self.address)
        return current_value

    @value.setter
    def value(self, value):
        if self.access_mode == AccessMode.READ_ONLY:
            raise Exception("Can't write to readonly register {} in {} address".format(self.name, self.address))
        self._i2c_connection.write_byte(self.device.address, value)
