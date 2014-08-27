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

    def is_collide(self, point):

        for offset in self.vertical_offsets:

            temp_x = copy.copy(point)
            temp_x.y += offset - self.camera_height
            if self.renderer.ground_collision(temp_x):

                return True

        return False

    def forward(self):

        next_x = self.camera.next_fw_x_point(self.collision_offset)
        next_z = self.camera.next_fw_z_point(self.collision_offset)

        # collide_x = False
        # for offset in self.vertical_offsets:
        #
        #     temp_x = copy.copy(next_x)
        #     temp_x.y += offset - self.camera_height
        #     if self.renderer.ground_collision(temp_x):
        #
        #         collide_x = True
        #         break

        if not self.is_collide(next_x):

            self.camera.forward_x()

        # collide_z = False
        # for offset in self.vertical_offsets:
        #
        #     temp_z = copy.copy(next_z)
        #     temp_z.y += offset - self.camera_height
        #     if self.renderer.ground_collision(temp_z):
        #
        #         collide_z = True
        #         break

        if not self.is_collide(next_z):

            self.camera.forward_z()

    def backward(self):

        next_x = self.camera.next_bw_x_point(self.collision_offset)
        next_z = self.camera.next_bw_z_point(self.collision_offset)

        # collide_x = False
        # for offset in self.vertical_offsets:
        #
        #     temp_x = copy.copy(next_x)
        #     temp_x.y += offset - self.camera_height
        #     if self.renderer.ground_collision(temp_x):
        #
        #         collide_x = True
        #         break

        if not self.is_collide(next_x):

            self.camera.backward_x()

        # collide_z = False
        # for offset in self.vertical_offsets:
        #
        #     temp_z = copy.copy(next_z)
        #     temp_z.y += offset - self.camera_height
        #     if self.renderer.ground_collision(temp_z):
        #
        #         collide_z = True
        #         break

        if not self.is_collide(next_z):

            self.camera.backward_z()

    def left(self):

        next_x = self.camera.next_left_x_point(self.collision_offset)
        next_z = self.camera.next_left_z_point(self.collision_offset)

        # collide_x = False
        # for offset in self.vertical_offsets:
        #
        #     temp_x = copy.copy(next_x)
        #     temp_x.y += offset - self.camera_height
        #     if self.renderer.ground_collision(temp_x):
        #
        #         collide_x = True
        #         break

        if not self.is_collide(next_x):

            self.camera.left_x()

        # collide_z = False
        # for offset in self.vertical_offsets:
        #
        #     temp_z = copy.copy(next_z)
        #     temp_z.y += offset - self.camera_height
        #     if self.renderer.ground_collision(temp_z):
        #
        #         collide_z = True
        #         break

        if not self.is_collide(next_z):

            self.camera.left_z()


class PlayerBody(Body):
    """Represents player's body in world."""

    pass
