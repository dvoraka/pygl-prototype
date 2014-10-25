# -*- coding: utf-8 -*-

"""Module for interfaces."""

from __future__ import print_function


class Creator(object):

    def create(self):

        raise NotImplementedError()

    def update(self):

        raise NotImplementedError()


class Configuration(object):

    def get_values(self):
        """Return configuration values.

        Return:
            dict: configuration values
        """

        raise NotImplementedError()
