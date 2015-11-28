__author__ = 'tmkasun'



class Pir(object):
    def __init__(self):
        self._x = None

    @property
    def x(self):
        print("I'm a property")
        if not self._x:
            return "No number"
        return self._x + 10

    @x.setter
    def x(self, value):
        print("I'm a property setter.\nI got {} value to set".format(value))
        self._x = value

    @x.deleter
    def x(self):
        print("I'm going...")

    def whoami(self):
        print(self.__class__)
