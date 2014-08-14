#! /usr/bin/env python

from __future__ import print_function

import re


class Script(object):

    def __init__(self, script_file):

        self.state = None

        self.token_pattern = r"""
(?P<command>\w+)
|(?P<multiplier>[0-9]+)
|(?P<newline>\n+)
|(?P<whitespace>[ \t]+)
"""

        self.tokenizer = Tokenizer(self.token_pattern)

        self.script_str = self.load_script(script_file)
        self.script_tokens = self.parse_script(self.script_str)
        self.token_index = 0

    def load_script(self, filename):

        with open(filename) as fo:

            script_str = fo.read()

        return script_str

    def parse_script(self, text):

        tokens = []
        for name, value in self.tokenizer.tokenize(text):

            tokens.append((name, value))

        return tokens

    def next_token(self):

        act_index = self.token_index
        self.token_index += 1

        if act_index >= len(self.script_tokens):

            return None

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

    script = Script("script.txt")

    while True:

        token = script.next_token()
        print(token)

        if not token:

            break
