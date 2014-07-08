# -*- coding: utf-8 -*-
#

"""Module for cameras."""

from math import sin
from math import cos
from math import pi
from numpy import matrix


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

        self.step = 0.2

    def v_angle_deg(self):

        return (self.v_angle * 180) / pi

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

    def forward(self):

        # self.z_pos += self.step

        pos_vec = self.get_position_vec()

        trans_matrix = matrix([
            [1.0, 0, 0, self.step * sin(self.v_angle)],
            [0, 1.0, 0, 0],
            [0, 0, 1.0, self.step * cos(self.v_angle)],
            [0, 0, 0, 1.0]
        ])

        result = trans_matrix * pos_vec
        self.set_position_vec(result)

    def backward(self):

        self.z_pos -= self.step

    def left(self):

        self.x_pos -= self.step

    def right(self):

        self.x_pos += self.step

    def up(self):
        
        self.y_pos += self.step

    def down(self):
        
        self.y_pos -= self.step
