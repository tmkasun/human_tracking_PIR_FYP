__author__ = 'tmkasun'

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory

import json
from config.parameters import configs, camera
from config.calibrate_camera import Calibrate
from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory

websocket_clients = []


class CoordinateUpdateProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))


    def onOpen(self):
        print("WebSocket connection open.")
        self.sendMessage("Welcome to KNNECT Websocket connector")
        websocket_clients.append(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


class CoordinateReciverProtocol(Protocol):
    def __init__(self):
        self.frame_count = 0
        self.calibrate = Calibrate(**camera)

    def connectionMade(self):
        self.transport.write("ACK")


    def dataReceived(self, data):
        """As soon as any data is received, write it back."""
        # print("Received request from: {}", data)
        # print(json.loads(data))
        self.frame_count += 1
        if self.frame_count % 10 == 0:
            frame_positions = json.loads(data)
            abs_locations = []
            for position in frame_positions:
                lat_lng = {'lat': position[0], 'lng': position[1]}
                abs_locations.append(self.calibrate.get_abs_position(lat_lng))
            for client in websocket_clients:
                client.sendMessage(json.dumps(abs_locations))
                # self.transport.write("ACK")


def main():
    # Websocket initializing

    ws_factory = WebSocketServerFactory(u"ws://{}:{}".format(configs['host'], configs['ws_port']), debug=False)
    ws_factory.protocol = CoordinateUpdateProtocol
    reactor.listenTCP(configs['ws_port'], ws_factory)
    print("Start Websocket server on ", configs['ws_port'])

    """This runs the protocol on port 8000"""
    factory = ServerFactory()
    factory.protocol = CoordinateReciverProtocol
    reactor.listenTCP(configs['service_port'], factory)
    print("Server started on port ", configs['service_port'])
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
