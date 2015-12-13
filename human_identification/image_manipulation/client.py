# # Copyright (c) University of Moratuwa
#
#
# """
# Client program to fetch PIR data from server and analyse the data
# """
#
# from twisted.internet import reactor, protocol
#
# from twisted.protocols.basic import LineReceiver
# import cv2
# import numpy as np
#
#
# class LocationDataProtocol(LineReceiver):
# """Once connected, fetch the thermal data and do analysis """
#
#     def connectionMade(self):
#         self.transport.write("ACK")
#
#     def dataReceived(self, data):
#         print("Data recived : {}".format(data))
#         # for i in range(100):
#         self.sendLine("ok")
#
#
#     def connectionLost(self, reason):
#         message_string = "Connection with {} through {} loss due to {} ".format(self.transport.addr[0],
#                                                                                 self.transport.addr[1], reason.value)
#         print(message_string)
#
#
# class PositionFactory(protocol.ClientFactory):
#     protocol = LocationDataProtocol
#
#     def clientConnectionFailed(self, connector, reason):
#         print "Connection failed - goodbye!"
#         reactor.stop()
#
#     def clientConnectionLost(self, connector, reason):
#         print "Connection lost - goodbye!"
#         reactor.stop()
#
#
# # this connects the protocol to a server running on port 8000
# def main():
#     f = PositionFactory()
#     reactor.connectTCP('127.0.0.1', 1234, f)
#     reactor.run()
#
# # this only runs if the module was *not* imported
# if __name__ == '__main__':
#     main()

