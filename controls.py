"""Module for controls infrastructure."""

from __future__ import print_function


class ControlsMapper(object):

    def __init__(self, filename):

        self.filename = filename

    def load_controls(self):

        pass

    def get_action(self, key):

        pass


class Controller(object):

    def __init__(self, controllable, controls_file):

        self.controllable_obj = controllable

        self.mapper = ControlsMapper(controls_file)

        self.actions = {
            "forward": self.controllable_obj.forward,
        }

    def update(self, key_state):

        pass