# -*- coding: utf-8 -*-
#

'''Module for cameras.'''


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

        self.v_angle = 0.0
        self.h_angle = 0.0

        self.step = 0.2

    def forward(self):

        self.z_pos += self.step

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
