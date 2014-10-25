#! /usr/bin/env python

"""Module for controls infrastructure."""

from __future__ import print_function

import ConfigParser
import os.path

from pyglet.window import key

from configuration import EngineConfiguration


class ControlsMapper(object):
    """Mapper class for controls.

    Args:
        filename (str): file with control schema

    Attributes:
        filename (str): file with control schema
        user_filename (str): user file with control schema (override filename)
        controls (dict): mapping action to keys
        pyglet_mapping (dict): pyglet keys mapping
    """

    def __init__(self, filename, user_filename):

        self.filename = filename
        self.user_filename = user_filename

        # default controls (when no config file is found)
        self.controls = self.get_default_controls()

        self.load_controls(self.filename)

        if os.path.isfile(self.user_filename):

            self.load_controls(self.user_filename)

        self.pyglet_mapping = self.get_pyglet_mapping()

    @staticmethod
    def get_default_controls():
        """Return default controls mapping as a dict.

        Return:
            dict: {"action": "key name"}
        """

        default_controls = {

            "forward": "W",
            "backward": "S",
            "left": "A",
            "right": "D",
            "jump": "Space",
        }

        return default_controls

    def load_controls(self, ini_file):
        """Load controls from file.

        Args:
            ini_file (str): ini file with controls
        """

        config = ConfigParser.ConfigParser()

        try:

            config.read(ini_file)

        except ConfigParser.ParsingError as err:

            print("Bad controls config file: {}".format(ini_file))
            print(err)

            return

        section = "Controls"

        self.set_value(config, section, "forward")
        self.set_value(config, section, "backward")
        self.set_value(config, section, "left")
        self.set_value(config, section, "right")
        self.set_value(config, section, "jump")

    def set_value(self, config, section, action):
        """Load configuration value and assign it.

        Args:
            config (ConfigParser): configuration parser
            section (str): section
            action (str): action
        """

        new_value = EngineConfiguration.config_value(config, section, action)

        if new_value:

            self.controls[action] = new_value

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

    @staticmethod
    def get_pyglet_mapping():
        """Return Pyglet mapping."""

        pyglet_mapping = {

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

        return pyglet_mapping


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
    print(cm.controls)
