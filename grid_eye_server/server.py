__author__ = 'tmkasun'

import threading
from twisted.internet import reactor
from twisted.internet.protocol import Protocol,ServerFactory
from libs.grideye import GridEye



class Echo(Protocol):
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
    factory = ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(8000, factory)
    print("Server sarted on port 8080")
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()