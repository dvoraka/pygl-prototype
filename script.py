#! /usr/bin/env python
#

"""Scripting module."""

from __future__ import print_function

import re


class Controllable(object):
    """Abstract class for controllable objects."""

    def forward(self):
        """Move forward."""

        raise NotImplementedError()

    def backward(self):
        """Move backward."""

        raise NotImplementedError()

    def left(self):
        """Move left."""

        raise NotImplementedError()

    def right(self):
        """Move right."""

        raise NotImplementedError()

    def up(self):
        """Move up."""

        raise NotImplementedError()

    def down(self):
        """Move down."""

        raise NotImplementedError()


class DummyObject(Controllable):
    """Simple testing class."""

    def forward(self):

        print("Moving forward...")

    def backward(self):

        print("Moving backward...")

    def left(self):

        print("Moving left...")

    def right(self):

        print("Moving right...")

    def up(self):

        print("Moving up...")

    def down(self):

        print("Moving down...")


class ScriptException(Exception):

    pass


class Script(object):
    """Class for scripts running.

    Args:
        script_file (str): script filename
        controllable_obj (Controllable): object for controlling
    """

    def __init__(self, script_file, controllable_obj):

        self.state = CommandState()

        self.controllable_obj = controllable_obj

        self.token_pattern = r"""
            (?P<command>[a-zA-Z]+)
            |(?P<float>[+-]?[0-9]+[.][0-9]+)
            |(?P<integer>[0-9]+)
            |(?P<hash>[#]+)
            |(?P<newline>\n)
            |(?P<whitespace>[ \t])
        """

        self.tokenizer = Tokenizer(self.token_pattern)

        self.script_str = self.load_script(script_file)
        self.script_tokens = self.analyze_script(self.script_str)
        self.token_index = 0

        self.stopped = False
        self.action_completed = False

    @staticmethod
    def load_script(filename):
        """Load script string from file.

        Args:
            filename (str): filename

        Return:
            str: script string
        """

        with open(filename) as fo:

            script_str = fo.read()

        return script_str

    def analyze_script(self, text):
        """Analyze script string.

        Args:
            text (str): script string

        Return:
            list of (token name, token value): script tokens
        """

        tokens = []
        for name, value in self.tokenizer.tokenize(text):

            tokens.append((name, value))

        return tokens

    def next_token(self):
        """Return token.

        Return:
            (token name, token value): token
        """

        act_index = self.token_index
        self.token_index += 1

        if act_index >= len(self.script_tokens):

            return None

        return self.script_tokens[act_index]

    def action_done(self):
        """Set action completed status."""

        self.action_completed = True

    def next_action(self):
        """Run next action.

        Return:
            True if next action exists
        """

        if not self.stopped:

            self.action_completed = False
            while not self.action_completed:

                new_state = self.next()

                if not new_state:

                    return False

        else:

            pass

        return True

    def next(self):
        """Transition to state.

        Return:
            ScriptState or None: next state
        """

        if self.state:

            self.state.process(self)

            # return new state
            return self.state

        else:

            return None

    def set_next_state(self, state):
        """Set next state.

        Args:
            state (ScriptState): new script state
        """

        self.state = state

    def start(self):
        """Start script."""

        self.stopped = False

    def stop(self):
        """Stop/pause script."""

        self.stopped = True

    def restart(self):
        """Restart script."""

        self.state = CommandState()

        self.token_index = 0
        self.action_completed = False

    def reload(self, script_file):

        # print("Reloading script file...")
        self.script_str = self.load_script(script_file)
        self.script_tokens = self.analyze_script(self.script_str)

        self.restart()


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

                elif token[0] == "integer":

                    # print("{} x {}".format(self.command, token[1]))
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

            # print("Processing {} ({})".format(self.command, self.multiplier))

            # action
            if self.command == "forward":

                context.controllable_obj.forward()

            elif self.command == "backward":

                context.controllable_obj.backward()

            elif self.command == "left":

                context.controllable_obj.left()

            elif self.command == "right":

                context.controllable_obj.right()

            elif self.command == "up":

                context.controllable_obj.up()

            elif self.command == "down":

                context.controllable_obj.down()

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
                "Tokenizer stopped at pos {} of {}".format(
                    position, len(text)))


if __name__ == "__main__":

    script = Script("script.txt", DummyObject())

    for token in script.script_tokens:

        print(token)

    # while script.next_action():
    #
    #     pass

    # while True:
    #
    #     val = script.next()
    #
    #     if not val:
    #
    #         break

    # while True:
    #
    #     token = script.next_token()
    #     print(token)
    #
    #     if not token:
    #
    #         break
