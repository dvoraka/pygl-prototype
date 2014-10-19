#!/usr/bin/env python
#
# Testing client for MP infrastructure
#

import time

import core
import data


test_size = 5

chunks = {}
creator = data.ChunkCreator(chunks)

z_position = 0
for _ in range(test_size):

    print("create")
    chunk_type = data.NormalChunk

    pos1 = data.Point(0, 0, z_position)
    pos2 = data.Point(0, 0, z_position)

    creator.create(chunk_type, pos1)
    creator.create(chunk_type, pos2)

    z_position += chunk_type.size

for _ in range(test_size * 2):

    print("update")
    creator.update()
    time.sleep(1)

creator.wait_for_procs()

print("Chunks: {}".format(chunks))
