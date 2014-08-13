from __future__ import print_function

import re


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


class TokenizerException(Exception):

    pass


class Tokenizer(object):
    """Class for token tools."""

    def __init__(self, pattern):

        self.token_pattern = pattern
        self.token_re = re.compile(self.token_pattern, re.VERBOSE)

    def tokenize(self, text):

        position = 0
        while True:

            match_obj = self.token_re.match(text, position)

            if not match_obj:

                break

            position = match_obj.end()

            token_name = match_obj.lastgroup
            token_value = match_obj.group(token_name)

            yield token_name, token_value

        if position != len(text):

            raise TokenizerException(
                "Tokenizer stopped at pos {} of {}".format(position, len(text)))
