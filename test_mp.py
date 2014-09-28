#!/usr/bin/env python
#
# Testing client for MP infrastructure
#

import time

import core
import data


vbos = []
vbo_creator = core.VboCreator(vbos)

chunk = data.NormalChunk(data.Point(0, 0, 0))
chunk2 = data.NormalChunk(data.Point(0, 0, 0))
chunk3 = data.NormalChunk(data.Point(0, 0, 0))

vbo_creator.create(chunk)
vbo_creator.create(chunk2)
vbo_creator.create(chunk3)

for _ in range(10):

    vbo_creator.check_parts()
    vbo_creator.build_ready_vbos()
    time.sleep(1)

vbo_creator.wait_for_procs()

print(vbos)
