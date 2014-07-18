# -*- coding: utf-8 -*-
#

"""Module for data representation."""

import random

import data


class Point(object):
    """Data for point."""

    def __init__(self, x, y, z):

        self.x = 0
        self.y = 0
        self.z = 0

        self.set_position(x, y, z)

    def __str__(self):

        return "Position: x={}, y={}, z={}".format(self.x, self.y, self.z)

    def set_position(self, x, y, z):
        """Set point position."""

        self.x = x
        self.y = y
        self.z = z


class Block(object):
    """Data representation for block."""

    def __init__(self):

        # real structure
        self.structure = None

        # lists of parents and children
        self.parents = None
        self.children = None

    def __str__(self):
        '''Return string representation.'''
        
        return 'Block'

    def __repr__(self):
        
        return self.__str__()


class Chunk(object):
    """Base class for chunks."""

    size = None
    height = None

    # chunk position in world
    position = None

    def __init__(self, position):

        self.blocks = None
        self.position = position

        self.blocks = self.generate_chunk()

    def generate_chunk(self):
        """Generate chunk data."""
        
        blocks = {}

        last = False
        for x in range(self.size):
            for y in range(self.height):
                for z in range(self.size):

                    if y < 50:

                        if last:
                            if random.randint(0, 2) in (0, 1):

                                blocks[(x, y, z)] = Block()
                                last = True

                            else:

                                blocks[(x, y, z)] = None
                                last = False

                        else:

                            if random.randint(0, 3) in (0,):

                                blocks[(x, y, z)] = Block()
                                last = True

                            else:

                                blocks[(x, y, z)] = None
                                last = False

                        # blocks[(x, y, z)] = Block()
                        # last = True

                    else:

                        blocks[(x, y, z)] = None

        return blocks

    def collision(self, point):

        counter = 0

        selected_blocks = []  # (x, y, z)

        for x in range(int(point.x - 2 - self.position.x), int(point.x + 2 - self.position.x)):
            for y in range(int(point.y - 2 - self.position.y), int(point.y + 2 - self.position.y)):
                for z in range(int(point.z - 2 - self.position.z), int(point.z + 2 - self.position.z)):

                    if x < 0 or x >= self.size:

                        pass

                    elif y < 0 or y >= self.height:

                        pass

                    elif z < 0 or z >= self.size:

                        pass

                    else:

                        selected_blocks.append((x, y, z))

        # for block in self.blocks:
        for block in selected_blocks:

            if abs(block[0] + self.position.x - point.x) < 0.5:
                if abs(block[1] + self.position.y - point.y) < 0.5:
                    if abs(block[2] + self.position.z - point.z) < 0.5:

                        if self.blocks[block] is not None:

                            # print("Collision: {}".format(block))
                            # print(counter)

                            return True

            counter += 1

        return False

    def __str__(self):
        """String representation of chunk."""
        
        return 'Chunk: ' + str(self.blocks)

    def __repr__(self):
        
        return self.__str__()


class SmallChunk(Chunk):
    """Small chunk of blocks - 2x2x128."""

    # size of chunk side
    size = 2
    # chunk height
    height = 128

    # def __init__(self):
    #     """Initialize small chunk."""
    #
    #     # blocks in chunk
    #     self.blocks = self.generate_chunk()

    def __str__(self):
        """String representation of chunk."""
        
        return 'SmallChunk: ' + str(self.blocks)


class NormalChunk(Chunk):

    # size of chunk side
    size = 8
    # chunk height
    height = 128
   
    # def __init__(self):
    #
    #     self.blocks = self.generate_chunk()


class BlockWorld:
    """World encapsulates blocks in chunks."""

    def __init__(self, chunk_type, width, depth):
        
        self.chunk_type = chunk_type
        self.chunk_size = self.chunk_type.size

        self.width = width
        self.depth = depth

        self.chunks = {}

        self.generate_world()

    def in_chunk(self, point):

        pass

    def collision(self, point):

        point.z = -point.z

        offset = 0.5

        counter = 0
        for chunk in self.chunks:

            if chunk[0] < point.x + offset and point.x - offset < chunk[0] + self.chunk_size:
                if chunk[1] < point.z + offset and point.z - offset < chunk[1] + self.chunk_size:

                    if self.chunks[chunk].collision(point):

                        # print(counter)
                        return True

            counter += 1

        return False

    def __str__(self):
        """String representation for world."""
        
        return 'BlockWorld: ' + str(self.chunks)

    def generate_world(self):
        """Generate world from chunks."""
        
        for x in range(0, self.width, self.chunk_size):
            for z in range(0, self.depth, self.chunk_size):

                self.chunks[(x, z)] = self.chunk_type(data.Point(x, 0, z))
