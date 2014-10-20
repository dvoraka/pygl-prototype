# -*- coding: utf-8 -*-

"""Module for configuration tools."""

from __future__ import print_function


class Configuration(object):

    def __init__(self):

        pass

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
