#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for configuration tools."""

from __future__ import print_function

import os
import ConfigParser

import interfaces


class EngineConfiguration(interfaces.Configuration):

    def __init__(self, filename, user_filename):

        self.filename = filename
        self.user_filename = user_filename

        # default values (when no config file is found)
        self.values = self.get_default_values()

        self.load_controls(self.filename)

        if os.path.isfile(self.user_filename):

            self.load_controls(self.user_filename)

    @staticmethod
    def get_default_values():
        """Return default values.

        Return:
            dict: {"key": "value"}
        """

        default_values = {

            "visibility": "22",
        }

        return default_values

    def get_values(self):

        return self.values

    def load_controls(self, ini_file):
        """Load configuration from file.

        Args:
            ini_file (str): ini file with controls
        """

        config = ConfigParser.ConfigParser()

        try:

            config.read(ini_file)

        except ConfigParser.ParsingError as err:

            print("Bad configuration file: {}".format(ini_file))
            print(err)

            return

        section = "Main"
        self.set_value(config, section, "visibility")

    def set_value(self, config, section, action):
        """Load configuration value and assign it.

        Args:
            config (ConfigParser): configuration parser
            section (str): section
            action (str): action
        """

        new_value = self.config_value(config, section, action)

        if new_value:

            self.values[action] = new_value

    @staticmethod
    def config_value(config, section, action):
        """Read configuration value.

        Args:
            config (ConfigParser: configuration parser
            section (str): section
            action (str): action

        Return:
            str or None: found value in configuration file
        """

        if config.has_section(section) and config.has_option(section, action):

            return config.get(section, action)


if __name__ == "__main__":

    conf = EngineConfiguration("settings.ini", "user.ini")
    print(conf.get_values())
