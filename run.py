#! /usr/bin/env python

import core
import graphics
import data

cw = data.BlockWorld(data.NormalChunk, 60, 80)
renderer = core.Renderer(cw)
renderer.prepare_world()

window = graphics.GameWindow(renderer)
window.show()
