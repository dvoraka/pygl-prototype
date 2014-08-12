"""Module for player's structures."""

from __future__ import print_function


class PlayerBody(object):
    """Represents player's body in world."""

    def __init__(self, camera, renderer, collision_offset, height):

        self.camera = camera
        self.renderer = renderer
        self.collision_offset = collision_offset

        self.height = height
        self.vertical_offsets = [self.height * 0.1, self.height * 0.9]

    def forward(self):

        next_x = self.camera.next_fw_x_point(self.collision_offset)
        next_z = self.camera.next_fw_z_point(self.collision_offset)

        collide_x = False
        for offset in self.vertical_offsets:

            temp_x = next_x
            temp_x.y += offset
            if self.renderer.ground_collision(temp_x):

                collide_x = True
                break

        if not collide_x:

            self.camera.forward_x()

        collide_z = False
        if not self.renderer.ground_collision(next_z):

            self.camera.forward_z()
