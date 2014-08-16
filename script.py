#! /usr/bin/env python

from __future__ import print_function

import re


class ScriptException(Exception):

    pass


class Script(object):

    def __init__(self, script_file):

        self.state = CommandState()

        self.token_pattern = r"""
(?P<command>[a-zA-Z]+)
|(?P<multiplier>[0-9]+)
|(?P<hash>[#]+)
|(?P<newline>\n)
|(?P<whitespace>[ \t])
"""

        self.tokenizer = Tokenizer(self.token_pattern)

        self.script_str = self.load_script(script_file)
        self.script_tokens = self.parse_script(self.script_str)
        self.token_index = 0

        self.action_completed = False

    @staticmethod
    def load_script(filename):

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

    def action_done(self):

        self.action_completed = True

    def next_action(self):

        self.action_completed = False
        while not self.action_completed:

            new_state = self.next()

            if not new_state:

                break

    def next(self):

        if self.state:

            self.state.process(self)

            # return new state
            return self.state

    def set_next_state(self, state):

        self.state = state


class CameraScript(Script):

    pass


class ScriptState(object):
    """Base class for script states."""

    def __init__(self):

        pass

    def process(self, context):

        pass


class CommandState(ScriptState):

    def process(self, context):

        while True:

            token = context.next_token()

            # print("Token: {}".format(token))

            if token:

                if token[0] == "whitespace":

                    continue

                elif token[0] == "newline":

                    continue

                elif token[0] == "command":

                    # print("Command: {}".format(token[1]))
                    context.set_next_state(MultiplierState(token[1]))

                    break

                elif token[0] == "hash":

                    context.set_next_state(CommentState())

                    break

            else:

                context.set_next_state(None)

                break


class MultiplierState(ScriptState):

    def __init__(self, command):

        super(MultiplierState, self).__init__()

        self.command = command

    def process(self, context):

        while True:

            token = context.next_token()

            # print("Token: {}".format(token))

            if token:

                if token[0] == "whitespace":

                    continue

                elif token[0] == "newline":

                    context.set_next_state(CommandState())

                    break

                elif token[0] == "multiplier":

                    print("{} x {}".format(self.command, token[1]))
                    context.set_next_state(
                        ProcessCommandState(self.command, int(token[1])))

                    break

            else:

                context.set_next_state(None)

                break


class CommentState(ScriptState):

    def process(self, context):

        while True:

            token = context.next_token()

            # print("Token: {}".format(token))

            if token:

                if token[0] == "newline":

                    context.set_next_state(CommandState())

                    break

            else:

                context.set_next_state(None)

                break


class ProcessCommandState(ScriptState):

    def __init__(self, command, multiplier):

        super(ProcessCommandState, self).__init__()

        self.command = command
        self.multiplier = multiplier

    def process(self, context):

        if self.multiplier > 0:

            print("Processing {} ({})".format(self.command, self.multiplier))

            # do something

            context.action_done()

            self.multiplier -= 1
            context.set_next_state(self)

        else:

            context.set_next_state(CommandState())


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

        val = script.next()

        if not val:

            break

    # while True:
    #
    #     token = script.next_token()
    #     print(token)
    #
    #     if not token:
    #
    #         break
