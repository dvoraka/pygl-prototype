#! /usr/bin/env python

import logging

import core
import graphics
import data


log = logging.getLogger(__name__)


def set_logger():

    logging.basicConfig(level=logging.DEBUG)


def main():

    log.info("Program start.")

    cw = data.BlockWorld(data.NormalChunk, 20, 20)
    renderer = core.Renderer(cw)
    renderer.prepare_world()

    window = graphics.GameWindow(renderer)
    window.show()

    log.info("Program exit.")


if __name__ == "__main__":

    set_logger()
    main()
