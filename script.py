#! /usr/bin/env python

from __future__ import print_function

import re


class Script(object):

    def __init__(self):

        self.state = None

        self.token_pattern = r"""
(?P<command>\w+)
|(?P<multiplier>[0-9]+)
|(?P<whitespace>\s+)
"""

        self.tokenizer = Tokenizer(self.token_pattern)

        self.script_str = self.load_script("script.txt")
        self.script_tokens = self.parse_script(self.script_str)
        self.token_index = 0

    def load_script(self, filename):

        script_str = open(filename).read()

        return script_str

    def parse_script(self, text):

        tokens = []
        for name, value in self.tokenizer.tokenize(text):

            tokens.append((name, value))

        return tokens

    def next_token(self):

        act_index = self.token_index
        self.token_index += 1

        return self.script_tokens[act_index]

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

if __name__ == "__main__":

    script = Script()

    print(script.next_token())
    print(script.next_token())
