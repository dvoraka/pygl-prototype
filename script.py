from __future__ import print_function


class Script(object):

    def __init__(self):

        self.state = None

    def next_token(self):

        pass

    def next(self):

        self.state.process(self)


class CameraScript(Script):

    pass


class ScriptState(object):
    """Base class for script states."""

    def process(self, context):

        pass
