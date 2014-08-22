#! /usr/bin/env python

"""Module for controls infrastructure."""

from __future__ import print_function

import ConfigParser
from pyglet.window import key


class ControlsMapper(object):

    def __init__(self, filename):

        self.filename = filename

        self.controls = {

            "forward": "A",
        }

        self.load_controls(self.filename)

        self.pyglet_mapping = {

            "A": key.A,
        }

        print(self.controls)

    def load_controls(self, ini_file):

        config = ConfigParser.ConfigParser()
        config.read(ini_file)

        section = "Controls"

        self.controls["forward"] = config.get(section, "forward")

    # def get_action(self, key):
    #
    #     pass

    def get_key(self, action):

        return self.pyglet_mapping[self.controls[action]]


class Controller(object):

    def __init__(self, controllable, controls_file):

        self.controllable_obj = controllable

        self.mapper = ControlsMapper(controls_file)

        self.actions = {

            "forward": self.controllable_obj.forward,
        }

    def update(self, key_state):

        if key_state[self.mapper.get_key("forward")]:

            self.actions["forward"]()


if __name__ == "__main__":

    cm = ControlsMapper("settings.ini")
