"""Module for player's structures."""

from __future__ import print_function


class PlayerBody(object):
    """Represents player's body in world."""

    def __init__(self, camera, renderer, collision_offset, height):

        self.camera = camera
        self.renderer = renderer
        self.collision_offset = collision_offset
        self.height = height

    def forward(self):

        next_x = self.camera.next_fw_x_point(self.collision_offset)
        next_z = self.camera.next_fw_z_point(self.collision_offset)

        if not self.renderer.ground_collision(next_x):

            self.camera.forward_x()

        if not self.renderer.ground_collision(next_z):

            self.camera.forward_z()
