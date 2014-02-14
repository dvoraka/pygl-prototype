# -*- coding: utf-8 -*-
#

'''Module for data representation.'''


class Block:
    '''Data representation for block.'''

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
    '''Base class for chunks.'''

    size = None
    height = None

    def __init__(self):

        self.blocks = None

    def generate_chunk(self):
        '''Generate chunk data.'''
        
        blocks = {}
        
        for x in range(self.size):
            for y in range(self.height):
                for z in range(self.size):

                    if y < 50:

                        blocks[(x, y, z)] = Block()

                    else:

                        blocks[(x, y, z)] = None

        return blocks

    def __str__(self):
        '''String representation of chunk.'''
        
        return 'Chunk: ' + str(self.blocks)

    def __repr__(self):
        
        return self.__str__()


class SmallChunk(Chunk):
    '''Small chunk of blocks - 2x2x128.'''

    # size of chunk side
    size = 2
    # chunk height
    height = 128

    def __init__(self):
        '''Initialize small chunk.'''

        # blocks in chunk
        self.blocks = self.generate_chunk()

    def __str__(self):
        '''String representation of chunk.'''
        
        return 'SmallChunk: ' + str(self.blocks)


class NormalChunk(Chunk):

    # size of chunk side
    size = 8
    # chunk height
    height = 128
   
    def __init__(self):
      
        self.blocks = self.generate_chunk()


class BlockWorld:
    '''World encapsulates blocks in chunks.'''

    def __init__(self, chunk_type, width, depth):
        
        self.chunk_type = chunk_type
        self.chunk_size = self.chunk_type.size

        self.width = width
        self.depth = depth

        self.chunks = {}

        self.generate_world()

    def __str__(self):
        '''String representation for world.'''
        
        return 'BlockWorld: ' + str(self.chunks)

    def generate_world(self):
        '''Generate world from chunks.'''
        
        for x in range(0, self.width, self.chunk_size):
            for z in range(0, self.depth, self.chunk_size):

                self.chunks[(x, z)] = self.chunk_type()