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


class FPSCamera:
    
    def __init__(
            self,
            x_pos=0.0,
            y_pos=0.0,
            z_pos=0.0,
            gravity=False):
        
        self.gravity = gravity
        self.falling = False
        self.falling_start = None
        self.fall_mp = 0.04

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

        # camera angles in radians
        self.v_angle = 0.0
        self.h_angle = 0.0

        self.v_multiplier = 0.01
        self.h_multiplier = 0.02

        self.inverse_horizontal = False

        self.h_angle_min = - pi / 3
        self.h_angle_max = pi / 3

        self.step = 0.02
        self.sprint_mp = 1.1
        self.side_step = self.step
        self.back_step = 0.2
        self.fly_step = 1.0

        self.helper_step = 0.1

    def position(self):

        #TODO: use cached object
        return data.Point(self.x_pos, self.y_pos, self.z_pos)

    def next_fw_x_point(self, offset=0.0):

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_coll_matrix(offset)

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_x = pos_list[0][0]

        return data.Point(next_x, self.y_pos, self.z_pos)

    def next_fw_z_point(self, offset=0.0):

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_coll_matrix(offset)

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_z = pos_list[2][0]

        return data.Point(self.x_pos, self.y_pos, next_z)

    def next_bw_x_point(self, offset=0.0):

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_coll_matrix(offset))

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_x = pos_list[0][0]

        return data.Point(next_x, self.y_pos, self.z_pos)

    def next_bw_z_point(self, offset=0.0):

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_coll_matrix(offset))

        result = trans_matrix * pos_vec

        pos_list = result.tolist()

        next_z = pos_list[2][0]

        return data.Point(self.x_pos, self.y_pos, next_z)

    def next_left_x_point(self, offset=0.0):

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.view_vec()
        new_vec = self.scale_matrix(self.side_step + offset) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        next_x = pos_list[0][0]

        return data.Point(next_x, self.y_pos, self.z_pos)

    def next_left_z_point(self, offset=0.0):

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.view_vec()
        new_vec = self.scale_matrix(self.side_step + offset) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        next_z = pos_list[2][0]

        return data.Point(self.x_pos, self.y_pos, next_z)

    def fall(self):

        now = time.time()

        if not self.falling:

            self.falling_start = now
            self.falling = True

        else:

            pass

        self.y_pos -= self.fall_mp * 5 * pow(now - self.falling_start, 2)

    def stop_falling(self):

        self.falling = False

    def v_angle_deg(self):

        return (self.v_angle * 180) / pi

    def h_angle_deg(self):

        return (self.h_angle * 180) / pi

    def add_v_angle(self, delta):

        self.v_angle += self.v_multiplier * delta

    def add_h_angle(self, delta):

        if self.inverse_horizontal:

            self.h_angle += self.h_multiplier * delta

        else:

            self.h_angle -= self.h_multiplier * delta

        if self.h_angle < self.h_angle_min:

            self.h_angle = self.h_angle_min

        elif self.h_angle > self.h_angle_max:

            self.h_angle = self.h_angle_max

    def get_position_vec(self):

        pos_vec = matrix([
            [self.x_pos],
            [self.y_pos],
            [self.z_pos],
            [1.0]
        ])

        return pos_vec

    def get_position_matrix(self):

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

    def fw_matrix(self):

        trans_matrix = matrix([
            [1.0, 0, 0, self.step * sin(self.v_angle)],
            [0, 1.0, 0, 0],
            [0, 0, 1.0, self.step * cos(self.v_angle)],
            [0, 0, 0, 1.0]
        ])

        return trans_matrix

    def fw_coll_matrix(self, offset=0.0):

        trans_matrix = matrix([
            [1.0, 0, 0, (self.step + offset) * sin(self.v_angle)],
            [0, 1.0, 0, 0],
            [0, 0, 1.0, (self.step + offset) * cos(self.v_angle)],
            [0, 0, 0, 1.0]
        ])

        return trans_matrix

    def right_matrix(self):

        trans_matrix = matrix([
            [1.0, 0, 0, self.step * sin(self.v_angle + pi / 2)],
            [0, 1.0, 0, 0],
            [0, 0, 1.0, self.step * cos(self.v_angle + pi / 2)],
            [0, 0, 0, 1.0]
        ])

        return trans_matrix

    def rot_y_matrix(self, angle):

        trans_matrix = matrix([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [- sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

        return trans_matrix

    def scale_matrix(self, ratio):

        trans_matrix = matrix([
            [ratio, 0, 0, 0],
            [0, ratio, 0, 0],
            [0, 0, ratio, 0],
            [0, 0, 0, 1]
        ])

        return trans_matrix

    def view_vec(self):

        vec = matrix([
            [sin(self.v_angle)],
            [0],
            [cos(self.v_angle)],
            [1]
        ])

        return vec

    def forward(self, sprint=False):

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_matrix()

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

        # pos_vec = self.get_position_vec()
        # trans_matrix = linalg.inv(self.right_matrix())
        #
        # result = trans_matrix * pos_vec
        # self.set_position_vec(result)

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec
        self.set_position_vec(result)

    def left_x(self):

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        x_pos = pos_list[0][0]

        self.set_position(data.Point(x_pos, self.y_pos, self.z_pos))

    def left_z(self):

        rot_m = self.rot_y_matrix(- pi / 2)
        new_vec = rot_m * self.view_vec()
        new_vec = self.scale_matrix(self.side_step) * new_vec

        result = self.get_position_matrix() * new_vec

        pos_list = result.tolist()
        z_pos = pos_list[2][0]

        self.set_position(data.Point(self.x_pos, self.y_pos, z_pos))

    def right(self):

        pos_vec = self.get_position_vec()
        trans_matrix = self.right_matrix()

        result = trans_matrix * pos_vec
        self.set_position_vec(result)

    def up(self):
        
        self.y_pos += self.fly_step

    def down(self):
        
        self.y_pos -= self.fly_step

    def collision_helper(self):

        self.y_pos += self.helper_step
