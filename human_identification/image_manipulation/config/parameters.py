import os

__author__ = 'tmkasun'

current_dir = os.path.dirname(__file__)

configs = {

    'current_dir': current_dir,
    'data_directory': current_dir + "/../../data/",
    'host': '127.0.0.1',
    'ws_port': 8001,
    'service_port': 9001
}

camera = {
    'abs_position': {'lat': 7.0709223267515116, 'lng': 79.9642068677349},
    'ops_abs_position': {'lat': 7.070942378703292, 'lng': 79.96429176069795},
    'frame_rate': 30,
    'frame_width': 428,
    'frame_height': 240
}