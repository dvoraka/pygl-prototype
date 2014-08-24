#! /usr/bin/env python

"""Module for controls infrastructure."""

from __future__ import print_function

import ConfigParser
from pyglet.window import key


class ControlsMapper(object):

    def __init__(self, filename):

        self.filename = filename

        # default controls (when no config file is found)
        self.controls = {

            "forward": "W",
            "backward": "S",
            "left": "A",
            "right": "D",
        }

        try:

            self.load_controls(self.filename)

        except ConfigParser.NoOptionError as e:

            print(e)
            print("Bad controls config.")

        self.pyglet_mapping = {

            "A": key.A,
            "B": key.B,
            "C": key.C,
            "D": key.D,
            "E": key.E,
            "F": key.F,
            "G": key.G,
            "H": key.H,
            "I": key.I,
            "J": key.J,
            "K": key.K,
            "L": key.L,
            "M": key.M,
            "O": key.O,
            "P": key.P,
            "Q": key.Q,
            "R": key.R,
            "S": key.S,
            "T": key.T,
            "U": key.U,
            "V": key.V,
            "W": key.W,
            "X": key.X,
            "Y": key.Y,
            "Z": key.Z,

            "UP": key.UP,
            "DOWN": key.DOWN,
            "LEFT": key.LEFT,
            "RIGHT": key.RIGHT,
        }

        print(self.controls)

    def load_controls(self, ini_file):

        config = ConfigParser.ConfigParser()

        try:

            config.read(ini_file)

        except ConfigParser.ParsingError as e:

            print("Bad controls config file: {}".format(ini_file))
            print(e)

            return

        section = "Controls"

        self.controls["forward"] = config.get(section, "forward")
        self.controls["backward"] = config.get(section, "backward")
        self.controls["left"] = config.get(section, "left")
        self.controls["right"] = config.get(section, "right")

    # def get_action(self, key):
    #
    #     pass

    def get_key(self, action):

        return self.pyglet_mapping[self.controls[action].upper()]


class Controller(object):

    def __init__(self, controllable, controls_file):

        self.controllable_obj = controllable

        self.mapper = ControlsMapper(controls_file)

        self.actions = {

            "forward": self.controllable_obj.forward,
            "backward": self.controllable_obj.backward,
            "left": self.controllable_obj.left,
            "right": self.controllable_obj.right,
        }

    def update(self, key_state):

        action = "forward"
        if key_state[self.get_key(action)]:

            self.actions[action]()

        action = "backward"
        if key_state[self.get_key(action)]:

            self.actions[action]()

        # action = "left"
        # if key_state[self.get_key(action)]:
        #
        #     self.actions[action]()

        # action = "right"
        # if key_state[self.get_key(action)]:
        #
        #     self.actions[action]()

    def get_key(self, action):

        return self.mapper.get_key(action)


if __name__ == "__main__":

    cm = ControlsMapper("settings.ini")
