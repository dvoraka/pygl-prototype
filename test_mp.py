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

for _ in range(test_size):

    print("create")
    creator.create(data.NormalChunk, data.Point(0, 0, 0))

for _ in range(test_size * 2):

    print("update")
    creator.update()
    time.sleep(1)

creator.wait_for_procs()

print("Chunks: {}".format(chunks))
