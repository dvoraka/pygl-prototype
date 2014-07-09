# -*- coding: utf-8 -*-
#

"""Module for cameras."""

from math import sin
from math import cos
from math import pi
from numpy import matrix
from numpy import linalg


class FPSCamera:
    
    def __init__(
            self,
            x_pos=0.0,
            y_pos=0.0,
            z_pos=0.0,
            gravity=False):
        
        self.gravity = gravity

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos

        # camera angles in radians
        self.v_angle = 0.0
        self.h_angle = 0.0

        self.v_multiplier = 0.05
        self.h_multiplier = 0.05

        self.step = 0.2

    def v_angle_deg(self):

        return (self.v_angle * 180) / pi

    def add_v_angle(self, delta):

        self.v_angle += self.v_multiplier * delta

    def add_h_angle(self, delta):

        self.h_angle -= self.h_multiplier * delta

    def get_position_vec(self):

        pos_vec = matrix([
            [self.x_pos],
            [self.y_pos],
            [self.z_pos],
            [1.0]
        ])

        return pos_vec

    def set_position_vec(self, position):

        pos_list = position.tolist()

        self.x_pos = pos_list[0][0]
        self.y_pos = pos_list[1][0]
        self.z_pos = pos_list[2][0]

    def fw_matrix(self):

        trans_matrix = matrix([
            [1.0, 0, 0, self.step * sin(self.v_angle)],
            [0, 1.0, 0, 0],
            [0, 0, 1.0, self.step * cos(self.v_angle)],
            [0, 0, 0, 1.0]
        ])

        return trans_matrix

    def forward(self):

        pos_vec = self.get_position_vec()
        trans_matrix = self.fw_matrix()

        result = trans_matrix * pos_vec
        self.set_position_vec(result)

    def backward(self):

        pos_vec = self.get_position_vec()
        trans_matrix = linalg.inv(self.fw_matrix())

        result = trans_matrix * pos_vec
        self.set_position_vec(result)

    def left(self):

        self.x_pos -= self.step

    def right(self):

        self.x_pos += self.step

    def up(self):
        
        self.y_pos += self.step

    def down(self):
        
        self.y_pos -= self.step
