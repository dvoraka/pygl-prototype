# -*- coding: utf-8 -*-
#

"""Module for cameras."""

import time

from math import sin
from math import cos
from math import pi
from numpy import matrix
from numpy import linalg

import data
import script


class FPSCamera(script.Controllable):

    def __init__(
            self,
            x_pos=0.0,
            y_pos=0.0,
            z_pos=0.0,
            gravity=False):

        # gravity attributes
        self.gravity = gravity
        # falling
        self.falling = False
        self.falling_start = None
        self.falling_mp = 0.0005
        self.falling_max_speed = 2.5

        self.jump_step_height = 0.17
        self.jump_steps = 16

        self.falling_counter = 0
        self.jump_counter = 0

        # camera position
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.position = data.Point(self.x_pos, self.y_pos, self.z_pos)

        # camera horizontal and vertical angles in radians
        self.h_angle = 0.0
        self.v_angle = 0.0

        # camera rotating sensitivity multipliers
        self.h_multiplier = 0.01
        self.v_multiplier = 0.02

        self.inverse_horizontal = False
        self.inverse_vertical = False

        # camera min and max vertical angles
        self.v_angle_min = - pi / 3
        self.v_angle_max = pi / 3

        self.step = 0.045
        self.sprint_mp = 1.8
        self.side_step = self.step
        self.back_step = 0.2
        self.fly_step = 1.0

        self.helper_step = 0.1

    def get_position(self):
        """Return camera position as a Point.

        Return:
            Point: the camera position
        """

        self.position.set_position(self.x_pos, self.y_pos, self.z_pos)

        return self.position

    def get_position_inverse_z(self):
        """Return camera position as a Point.

        Return:
            Point: the camera position with inverse z axis
        """

        position = self.get_position()
        position.z = - position.z

        return position

    def next_fw_x_point(self, offset=0.0):
        """Return next forward x axis Point."""

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_coll_matrix(offset)

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_x = pos_list[0][0]

        return data.Point(next_x, self.y_pos, self.z_pos)

    def next_fw_z_point(self, offset=0.0):
        """Return next forward z axis Point."""

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_coll_matrix(offset)

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_z = pos_list[2][0]

        return data.Point(self.x_pos, self.y_pos, next_z)

    def next_bw_x_point(self, offset=0.0):
        """Return next backward x axis Point."""

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_coll_matrix(offset))

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_x = pos_list[0][0]

        return data.Point(next_x, self.y_pos, self.z_pos)

    def next_bw_z_point(self, offset=0.0):
        """Return next backward z axis Point."""

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_coll_matrix(offset))

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_z = pos_list[2][0]

        return data.Point(self.x_pos, self.y_pos, next_z)

    def next_left_x_point(self, offset=0.0):
        """Return next left x axis Point."""

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step + offset) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        next_x = pos_list[0][0]

        return data.Point(next_x, self.y_pos, self.z_pos)

    def next_left_z_point(self, offset=0.0):
        """Return next left z axis Point."""

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step + offset) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        next_z = pos_list[2][0]

        return data.Point(self.x_pos, self.y_pos, next_z)

    def next_right_x_point(self, offset=0.0):

        rot_m = self.rot_y_matrix(pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step + offset) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        next_x = pos_list[0][0]

        return data.Point(next_x, self.y_pos, self.z_pos)

    def next_right_z_point(self, offset=0.0):

        rot_m = self.rot_y_matrix(pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step + offset) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        next_z = pos_list[2][0]

        return data.Point(self.x_pos, self.y_pos, next_z)

    def jump(self):

        if self.jump_counter == 0:

            self.jump_counter = 1
            self.y_pos += self.jump_step_height

    def fall(self):
        """Simulate camera falling."""

        # now = time.time()

        if not self.falling:

            # self.falling_start = now
            self.falling = True
            self.falling_counter = 0

        else:

            pass

        if 0 < self.jump_counter < self.jump_steps:

            self.y_pos += self.jump_step_height
            self.jump_counter += 1

        # falling_step = self.falling_mp * 5 * pow(now - self.falling_start, 2)
        falling_step = self.falling_mp * 5 * pow(self.falling_counter, 2)

        # print(falling_step)
        if falling_step > self.falling_max_speed:

            falling_step = self.falling_max_speed

        self.y_pos -= falling_step
        self.falling_counter += 1

    def stop_falling(self):
        """Stop camera falling."""

        self.falling = False

    def h_angle_deg(self):
        """Return camera horizontal angle in degrees."""

        return (self.h_angle * 180) / pi

    def v_angle_deg(self):
        """Return camera vertical angle in degrees."""

        return (self.v_angle * 180) / pi

    def add_h_angle(self, delta):
        """Add delta value to horizontal angle.

        Args:
            delta (float): delta value
        """

        self.h_angle += self.h_multiplier * delta

    def add_v_angle(self, delta):
        """Add delta value to vertical angle.

        Args:
            delta (float): delta value
        """

        if self.inverse_horizontal:

            self.v_angle += self.v_multiplier * delta

        else:

            self.v_angle -= self.v_multiplier * delta

        if self.v_angle < self.v_angle_min:

            self.v_angle = self.v_angle_min

        elif self.v_angle > self.v_angle_max:

            self.v_angle = self.v_angle_max

    def get_position_vec(self):
        """Return position vector.

        Return:
            matrix: position vector
        """

        pos_vec = matrix([
            [self.x_pos],
            [self.y_pos],
            [self.z_pos],
            [1.0]
        ])

        return pos_vec

    def get_position_matrix(self):
        """Return position matrix.

        Return:
            matrix: translation position matrix
        """

        pos_matrix = matrix([
            [1.0, 0, 0, self.x_pos],
            [0, 1.0, 0, self.y_pos],
            [0, 0, 1.0, self.z_pos],
            [0, 0, 0, 1.0]
        ])

        return pos_matrix

    def set_position_vec(self, position):

        pos_list = position.tolist()

        self.x_pos = pos_list[0][0]
        self.y_pos = pos_list[1][0]
        self.z_pos = pos_list[2][0]

    def set_position(self, point):

        self.x_pos = point.x
        self.y_pos = point.y
        self.z_pos = point.z

    def fw_matrix(self, sprint=False):

        if sprint:
            # use sprint multiplier
            trans_matrix = matrix([
                [1.0, 0, 0, (self.step * self.sprint_mp) * sin(self.h_angle)],
                [0, 1.0, 0, 0],
                [0, 0, 1.0, (self.step * self.sprint_mp) * cos(self.h_angle)],
                [0, 0, 0, 1.0]
            ])

        else:

            trans_matrix = matrix([
                [1.0, 0, 0, self.step * sin(self.h_angle)],
                [0, 1.0, 0, 0],
                [0, 0, 1.0, self.step * cos(self.h_angle)],
                [0, 0, 0, 1.0]
            ])

        return trans_matrix

    def fw_coll_matrix(self, offset=0.0):

        trans_matrix = matrix([
            [1.0, 0, 0, (self.step + offset) * sin(self.h_angle)],
            [0, 1.0, 0, 0],
            [0, 0, 1.0, (self.step + offset) * cos(self.h_angle)],
            [0, 0, 0, 1.0]
        ])

        return trans_matrix

    def right_matrix(self):

        trans_matrix = matrix([
            [1.0, 0, 0, self.step * sin(self.h_angle + pi / 2)],
            [0, 1.0, 0, 0],
            [0, 0, 1.0, self.step * cos(self.h_angle + pi / 2)],
            [0, 0, 0, 1.0]
        ])

        return trans_matrix

    @staticmethod
    def rot_y_matrix(angle):

        trans_matrix = matrix([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [- sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

        return trans_matrix

    @staticmethod
    def scale_matrix(ratio):

        trans_matrix = matrix([
            [ratio, 0, 0, 0],
            [0, ratio, 0, 0],
            [0, 0, ratio, 0],
            [0, 0, 0, 1]
        ])

        return trans_matrix

    def view_vec(self):
        """Return view vector."""

        #TODO: implementation
        raise NotImplementedError

    def horizontal_view_vec(self):
        """Return horizontal view vector.

        Return:
            matrix: view vector
        """

        vec = matrix([
            [sin(self.h_angle)],
            [0],
            [cos(self.h_angle)],
            [1]
        ])

        return vec

    def forward(self, sprint=False):

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_matrix(sprint)

        result = trans_matrix * pos_vec
        self.set_position_vec(result)

    def forward_x(self):

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_matrix()

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        x_pos = pos_list[0][0]

        self.set_position(data.Point(x_pos, self.y_pos, self.z_pos))

    def forward_z(self):

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_matrix()

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        z_pos = pos_list[2][0]

        self.set_position(data.Point(self.x_pos, self.y_pos, z_pos))

    def sprint(self):

        self.forward(sprint=True)

    def backward(self):

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_matrix())

        result = trans_matrix * pos_vec
        self.set_position_vec(result)

    def backward_x(self):

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_matrix())

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        x_pos = pos_list[0][0]

        self.set_position(data.Point(x_pos, self.y_pos, self.z_pos))

    def backward_z(self):

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_matrix())

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        z_pos = pos_list[2][0]

        self.set_position(data.Point(self.x_pos, self.y_pos, z_pos))

    def left(self):
        """Move camera left."""

        # pos_vec = self.get_position_vec()
        # trans_matrix = linalg.inv(self.right_matrix())
        #
        # result = trans_matrix * pos_vec
        # self.set_position_vec(result)

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec
        self.set_position_vec(result)

    def left_x(self):

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        x_pos = pos_list[0][0]

        self.set_position(data.Point(x_pos, self.y_pos, self.z_pos))

    def left_z(self):

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        z_pos = pos_list[2][0]

        self.set_position(data.Point(self.x_pos, self.y_pos, z_pos))

    def right(self):
        """Move camera right."""

        pos_vec = self.get_position_vec()
        trans_matrix = self.right_matrix()

        result = trans_matrix * pos_vec
        self.set_position_vec(result)

    def right_x(self):
        """Move camera right in x axis."""

        rot_m = self.rot_y_matrix(pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        x_pos = pos_list[0][0]

        self.set_position(data.Point(x_pos, self.y_pos, self.z_pos))

    def right_z(self):
        """Move camera right in z axis."""

        rot_m = self.rot_y_matrix(pi / 2)
        new_vec = rot_m * self.horizontal_view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        z_pos = pos_list[2][0]

        self.set_position(data.Point(self.x_pos, self.y_pos, z_pos))

    def up(self):
        """Move camera up."""

        self.y_pos += self.fly_step

    def down(self):
        """Move camera down."""

        self.y_pos -= self.fly_step

    def collision_helper(self):
        """Help camera with in-block collisions."""

        self.y_pos += self.helper_step

    def set_gravity(self, gravity):

        self.gravity = gravity
