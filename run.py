#! /usr/bin/env python

import graphics
import data

cw = data.BlockWorld(data.NormalChunk, 20, 60)
renderer = graphics.Renderer(cw)
renderer.prepare_world()

window = graphics.GameWindow(renderer)
window.show()
