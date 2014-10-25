#! /usr/bin/env python

import logging

import core
import graphics
import data
import configuration


log = logging.getLogger(__name__)


def set_logger():

    logging.basicConfig(level=logging.DEBUG)


def main():

    log.info("Program start.")

    cw = data.BlockWorld(data.NormalChunk, 20, 20)
    conf = configuration.EngineConfiguration("settings.ini", "user.ini")
    renderer = core.Renderer(cw, conf)
    renderer.prepare_world()

    window = graphics.GameWindow(renderer)
    window.show()

    log.info("Program exit.")


if __name__ == "__main__":

    set_logger()
    main()
