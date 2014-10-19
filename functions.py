# -*- coding: utf-8 -*-

"""Module for functions."""

from __future__ import print_function

import random

import data

from decorators import print_time


def generate_chunk_mp(position, width, height):

    blocks = generate_chunk(width, height)

    return position, blocks


@print_time
def generate_chunk(width, height):
    """Generate chunk data.

    Args:
        width (int): width
        height (int): height

    Return:
        dict: {(x, y, z) of int: Block}
    """

    blocks = {}

    last = False
    for x in range(width):
        for y in range(height):
            for z in range(width):

                if y < 50:

                    if last:
                        if random.randint(0, 2) in (0, 1):

                            blocks[(x, y, z)] = data.Block()
                            last = True

                        else:

                            blocks[(x, y, z)] = None
                            last = False

                    else:

                        if random.randint(0, 3) in (0,):

                            blocks[(x, y, z)] = data.Block()
                            last = True

                        else:

                            blocks[(x, y, z)] = None
                            last = False

                else:

                    blocks[(x, y, z)] = None

    return blocks
