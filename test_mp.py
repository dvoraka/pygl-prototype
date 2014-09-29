#!/usr/bin/env python
#
# Testing client for MP infrastructure
#

import time

import core
import data


test_size = 10

vbos = []
vbo_creator = core.VboCreator(vbos)

for _ in range(test_size):

    vbo_creator.create(data.NormalChunk(data.Point(0, 0, 0)))

for _ in range(10):

    vbo_creator.check_parts()
    vbo_creator.build_ready_vbos()
    time.sleep(1)

vbo_creator.wait_for_procs()

print("Ready VBOs: {}".format(len(vbo_creator.ready_vbos)))

# print(vbos)
