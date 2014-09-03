#! /usr/bin/env python

"""Module for controls infrastructure."""

from __future__ import print_function

import ConfigParser
import os.path

from pyglet.window import key


class ControlsMapper(object):
    """Mapper class for controls.

    Args:
        filename (str): file with control schema

    Attributes:
        filename (str): file with control schema
        controls (dict): mapping action to keys
        pyglet_mapping (dict): pyglet keys mapping
    """

    def __init__(self, filename, user_filename):

        self.filename = filename
        self.user_filename = user_filename

        # default controls (when no config file is found)
        self.controls = {

            "forward": "W",
            "backward": "S",
            "left": "A",
            "right": "D",
            "jump": "Space",
        }

        try:

            self.load_controls(self.filename)

        except ConfigParser.NoOptionError as e:

            print(e)
            print("Bad controls config.")

        if os.path.isfile(self.user_filename):

            try:

                self.load_controls(self.user_filename)

            except ConfigParser.NoOptionError as e:

                print(e)
                print("Bad user controls config.")

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
            "SPACE": key.SPACE,
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

        # self.controls["forward"] = self.config_value(config, section, "forward")
        self.set_value(config, section, "forward")
        # self.controls["backward"] = config.get(section, "backward")
        self.set_value(config, section, "backward")

        self.controls["left"] = config.get(section, "left")
        self.controls["right"] = config.get(section, "right")
        self.controls["jump"] = config.get(section, "jump")

    def set_value(self, config, section, action):

        new_value = self.config_value(config, section, action)

        if new_value:

            self.controls[action] = new_value

    def config_value(self, config, section, action):

        if config.has_section(section) and config.has_option(section, action):

            return config.get(section, action)

    def get_pyglet_action(self, pyglet_key):
        """Return mapped action to the pyglet key."""

        pass

    def get_pyglet_key(self, action):
        """Return Pyglet key for action.

        Args:
            action (str): action

        Return:
            int: key constant
        """

        return self.pyglet_mapping[self.controls[action].upper()]


class Controller(object):
    """Class for objects controlling.

    Args:
        controllable (interfaces.Controllable): object for controlling
        controls_file (str): configuration file

    Attributes:
        controllable_obj (interfaces.Controllable): object for controlling
        mapper (ControlsMapper): mapper
        actions (dict): map actions names to methods
    """

    def __init__(self, controllable, controls_file, user_file="user.ini"):

        self.controllable_obj = controllable

        self.mapper = ControlsMapper(controls_file, user_file)

        self.actions = {

            "fall": self.controllable_obj.fall,
            "forward": self.controllable_obj.forward,
            "backward": self.controllable_obj.backward,
            "left": self.controllable_obj.left,
            "right": self.controllable_obj.right,
            "jump": self.controllable_obj.jump,
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

        action = "right"
        if key_state[self.get_pyglet_key(action)]:

            self.actions[action]()

        action = "jump"
        if key_state[self.get_pyglet_key(action)]:

            self.actions[action]()

    def get_pyglet_key(self, action):
        """Return Pyglet key for the action.

        Args:
            action (str): the action

        Return:
            int: key constant
        """

        return self.mapper.get_pyglet_key(action)


if __name__ == "__main__":

    cm = ControlsMapper("settings.ini", "user.ini")
