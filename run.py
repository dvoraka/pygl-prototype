#! /usr/bin/env python

import core
import graphics
import data

cw = data.BlockWorld(data.NormalChunk, 20, 20)
renderer = core.Renderer(cw)
renderer.prepare_world()

window = graphics.GameWindow(renderer)
window.show()
