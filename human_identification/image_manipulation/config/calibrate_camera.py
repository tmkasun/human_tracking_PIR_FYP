__author__ = 'tmkasun'


class Calibrate(object):
    def __init__(self, abs_position, ops_abs_position, frame_rate, frame_width, frame_height):
        self.abs_position = abs_position
        self.frame_rate = frame_rate
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.ops_abs_position = ops_abs_position
        self.lat_grad = None
        self.lng_grad = None
        self.setup_gradients()

    def setup_gradients(self):
        lat_diff = (self.abs_position['lat'] - self.ops_abs_position['lat'])
        self.lat_grad = lat_diff * 0.3 / 428

        lng_diff = (self.abs_position['lng'] - self.ops_abs_position['lng'])
        self.lng_grad = lng_diff * 0.3 / 240

    def get_abs_position(self, relative_position):
        abs_lat = self.abs_position['lat'] + self.lat_grad * relative_position['lng']  # TODO: Wrong mapping of lat and lng
        abs_lng = self.abs_position['lng'] + self.lng_grad * relative_position['lat']
        return {'lat': abs_lat, 'lng': abs_lng}