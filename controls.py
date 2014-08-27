#! /usr/bin/env python

"""Module for controls infrastructure."""

from __future__ import print_function

import ConfigParser
from pyglet.window import key


class ControlsMapper(object):
    """Mapper class for controls.

    Args:
        filename (str): file with control schema
    """

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
        """Load controls from file.

        Args:
            ini_file (str): ini file with controls
        """

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

    def get_pyglet_key(self, action):
        """Return Pyglet key for action.

        Args:
            action (str): action
        """

        return self.pyglet_mapping[self.controls[action].upper()]


class Controller(object):
    """Class for objects controlling.

    Args:
        controllable (interfaces.Controllable): object for controlling
        controls_file (str): configuration file
    """

    def __init__(self, controllable, controls_file):

        self.controllable_obj = controllable

        self.mapper = ControlsMapper(controls_file)

        self.actions = {

            "fall": self.controllable_obj.fall,
            "forward": self.controllable_obj.forward,
            "backward": self.controllable_obj.backward,
            "left": self.controllable_obj.left,
            "right": self.controllable_obj.right,
        }

    def update(self, key_state):
        """Call actions according to key states.

        Args:
            key_state (dict): keys states
        """

        # gravity
        self.actions["fall"]()

        action = "forward"
        if key_state[self.get_pyglet_key(action)]:

            self.actions[action]()

        action = "backward"
        if key_state[self.get_pyglet_key(action)]:

            self.actions[action]()

        action = "left"
        if key_state[self.get_pyglet_key(action)]:

            self.actions[action]()

        # action = "right"
        # if key_state[self.get_key(action)]:
        #
        #     self.actions[action]()

    def get_pyglet_key(self, action):
        """Return Pyglet key for action.

        Args:
            action (str): action
        """

        return self.mapper.get_pyglet_key(action)


if __name__ == "__main__":

    cm = ControlsMapper("settings.ini")
