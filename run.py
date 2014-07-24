#! /usr/bin/env python

import graphics
import data

cw = data.BlockWorld(data.NormalChunk, 60, 80)
renderer = graphics.Renderer(cw)
renderer.prepare_world()

window = graphics.GameWindow(renderer)
window.show()
