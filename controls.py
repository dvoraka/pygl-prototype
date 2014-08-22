"""Module for controls infrastructure."""

from __future__ import print_function

from pyglet.window import key


class ControlsMapper(object):

    def __init__(self, filename):

        self.filename = filename

        self.controls = {
            "forward": key.A,
        }

    def load_controls(self):

        pass

    # def get_action(self, key):
    #
    #     pass

    def get_key(self, action):

        return self.controls[action]


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
