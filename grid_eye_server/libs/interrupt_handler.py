__author__ = 'tmkasun'

from register import Register, AccessMode


class InterruptHandler(object):
    def __init__(self, device):
        self.device = device