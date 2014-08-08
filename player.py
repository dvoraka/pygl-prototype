"""Module for player's structures."""

from __future__ import print_function


class PlayerBody(object):
    """Represents player's body in world."""

    def __init__(self, camera, height):

        self.camera = camera
        self.height = height