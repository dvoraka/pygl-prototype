"""Module for player's structures."""

from __future__ import print_function

import copy


class PlayerBody(object):
    """Represents player's body in world."""

    def __init__(self, camera, renderer, collision_offset, height):

        self.camera = camera
        self.renderer = renderer
        self.collision_offset = collision_offset

        self.height = height
        # static for now
        self.vertical_offsets = [0.1, 1.1]

    def forward(self):

        next_x = self.camera.next_fw_x_point(self.collision_offset)
        next_z = self.camera.next_fw_z_point(self.collision_offset)

        collide_x = False
        for offset in self.vertical_offsets:

            temp_x = copy.copy(next_x)
            temp_x.y += offset
            if self.renderer.ground_collision(temp_x):

                collide_x = True
                break

        if not collide_x:

            self.camera.forward_x()

        collide_z = False
        for offset in self.vertical_offsets:

            temp_z = copy.copy(next_z)
            temp_z.y += offset
            if self.renderer.ground_collision(temp_z):

                collide_z = True
                break

        if not collide_z:

            self.camera.forward_z()
