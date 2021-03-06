"""Module for player's structures."""

from __future__ import print_function

import copy

import data
import script


class Body(script.Controllable):
    """Represents body in world."""

    def __init__(self, camera, renderer, collision_offset, height):

        self.camera = camera
        self.camera_fall_collision = False

        self.renderer = renderer
        self.collision_offset = collision_offset

        self.height = height
        self.camera_height = self.height * 0.9

        # static for now
        self.vertical_offsets = [0.2, 1.2]

    def fall(self):

        position = data.Point(
            self.camera.x_pos,
            self.camera.y_pos - self.camera_height,
            self.camera.z_pos)
        position2 = data.Point(
            self.camera.x_pos,
            self.camera.y_pos - (self.height * 0.8),
            self.camera.z_pos)

        if self.renderer.ground_collision(position2):

            # print("helper")
            self.camera.collision_helper()
            self.camera.stop_falling()
            self.camera_fall_collision = True

        elif self.renderer.ground_collision(position):

            self.camera.stop_falling()
            self.camera_fall_collision = True

        else:

            self.camera_fall_collision = False

        if self.camera.gravity and not self.camera_fall_collision:

            self.camera.fall()

        else:

            self.camera.jump_counter = 0

    def is_collide(self, point):
        """Check collision for point and all its vertical offsets.

        Args:
            point (data.Point): point

        Return:
            bool: collision
        """

        for offset in self.vertical_offsets:

            temp = copy.copy(point)
            temp.y += offset - self.camera_height

            if self.renderer.ground_collision(temp):

                return True

        return False

    def forward(self):

        next_x = self.camera.next_fw_x_point(self.collision_offset)
        next_z = self.camera.next_fw_z_point(self.collision_offset)

        if not self.is_collide(next_x):

            self.camera.forward_x()

        if not self.is_collide(next_z):

            self.camera.forward_z()

    def backward(self):

        next_x = self.camera.next_bw_x_point(self.collision_offset)
        next_z = self.camera.next_bw_z_point(self.collision_offset)

        if not self.is_collide(next_x):

            self.camera.backward_x()

        if not self.is_collide(next_z):

            self.camera.backward_z()

    def left(self):

        next_x = self.camera.next_left_x_point(self.collision_offset)
        next_z = self.camera.next_left_z_point(self.collision_offset)

        if not self.is_collide(next_x):

            self.camera.left_x()

        if not self.is_collide(next_z):

            self.camera.left_z()

    def right(self):

        next_x = self.camera.next_right_x_point(self.collision_offset)
        next_z = self.camera.next_right_z_point(self.collision_offset)

        if not self.is_collide(next_x):

            self.camera.right_x()

        if not self.is_collide(next_z):

            self.camera.right_z()

    def jump(self):

        # camera_position = self.camera.get_position_inverse_z()
        camera_position = self.camera.get_position()
        camera_position.y += 0.6
        new_position = camera_position

        if not self.renderer.ground_collision(new_position):

            self.camera.jump()


class PlayerBody(Body):
    """Represents player's body in world."""

    pass
