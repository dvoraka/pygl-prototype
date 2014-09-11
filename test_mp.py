#!/usr/bin/env python
#
# Testing client for MP infrastructure
#

import core
import data


vbos = []
vbo_creator = core.VboCreator(vbos)

chunk = data.NormalChunk(data.Point(0, 0, 0))
chunk2 = data.NormalChunk(data.Point(0, 0, 0))

vbo_creator.create(chunk)
vbo_creator.create(chunk2)

vbo_creator.wait_for_procs()

print(vbos)
