# -*- coding: utf-8 -*-
#

"""Module for data representation."""

import random
import uuid

from math import sqrt


class Point(object):
    """Store data for point in 3D space.

    Args:
        x (float): x position
        y (float): y position
        z (float): z position
    """

    def __init__(self, x, y, z):

        self.x = 0
        self.y = 0
        self.z = 0

        self.set_position(x, y, z)

    def __str__(self):
        """Return string representation."""

        return "Position: x={}, y={}, z={}".format(self.x, self.y, self.z)

    def set_position(self, x, y, z):
        """Set point position."""

        self.x = x
        self.y = y
        self.z = z

    def chunk_distance(self, chunk_pos):
        """Return distance of chunk from self instance.

        Args:
            chunk_pos (Point): position of chunk
        """

        x_dist = chunk_pos.x - self.x
        z_dist = chunk_pos.z - self.z

        distance = sqrt(pow(x_dist, 2) + pow(z_dist, 2))

        return distance


class Block(object):
    """Data representation for block.

    Attributes:
        structure: block structure
        parents (list): block's parents
        children (list): block's children
    """

    def __init__(self):

        # real structure
        self.structure = None

        # lists of parents and children
        self.parents = None
        self.children = None

    def __str__(self):
        """Return string representation."""

        return 'Block'

    def __repr__(self):

        return self.__str__()


class BlockInfo(object):
    """Auxiliary mapping class.

    Args:
        chunk (Chunk): chunk object
        position ((x, y, z)): position of block

    Attributes:
        position ((x, y, z)): position of block
        chunk_id (str): ID of chunk
        chunk_position (Point): position of chunk
    """

    def __init__(self, chunk, position):

        self.position = position
        self.chunk_id = chunk.chunk_id
        self.chunk_position = chunk.position


class Chunk(object):
    """Base class for chunks.

    Args:
        position (Point): position of chunk

    Attributes:
        position (Position): position of chunk
        centre (Point): centre point of chunk
        chunk_id (str): ID of chunk
        dirty (bool): indicates changes in chunk
        visible (bool): stores visibility for chunk
        blocks (dict): dictionary of Block objects, key is (x, y, z) of int
    """

    size = None
    height = None

    def __init__(self, position):

        self.position = position
        self.centre = Point(
            position.x + self.size / 2,
            0,
            position.z + self.size / 2
        )

        self.chunk_id = str(uuid.uuid4())

        self.dirty = False
        self.visible = False

        self.blocks = self.generate_chunk()

    def get_centre(self):
        """Return centre of chunk as a Point object."""

        return self.centre

    def generate_chunk(self):
        """Generate chunk data.

        Return:
            dict: {(x, y, z) of int: Block}
        """

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

                    else:

                        blocks[(x, y, z)] = None

        return blocks

    def block_collision(self, point):
        """Return collision block info.

        Args:
            point (Point): the collision point

        Return:
            BlockInfo or None: info about block
        """

        selected_blocks = []  # (x, y, z)
        for x in range(int(point.x - 2 - self.position.x),
                       int(point.x + 2 - self.position.x)):
            for y in range(int(point.y - 2 - self.position.y),
                           int(point.y + 2 - self.position.y)):
                for z in range(int(point.z - 2 - self.position.z),
                               int(point.z + 2 - self.position.z)):

                    if x < 0 or x >= self.size:

                        pass

                    elif y < 0 or y >= self.height:

                        pass

                    elif z < 0 or z >= self.size:

                        pass

                    else:

                        selected_blocks.append((x, y, z))

        for block in selected_blocks:

            if abs(block[0] + self.position.x - point.x) < 0.5:
                if abs(block[1] + self.position.y - point.y) < 0.5:
                    if abs(block[2] + self.position.z - point.z) < 0.5:

                        if self.blocks[block] is not None:

                            return BlockInfo(self, block)

        return None

    def collision(self, point):
        """Return boolean value of collision for the point."""

        # debug info
        # counter = 0

        selected_blocks = []  # (x, y, z)

        for x in range(int(point.x - 2 - self.position.x),
                       int(point.x + 2 - self.position.x)):
            for y in range(int(point.y - 2 - self.position.y),
                           int(point.y + 2 - self.position.y)):
                for z in range(int(point.z - 2 - self.position.z),
                               int(point.z + 2 - self.position.z)):

                    if x < 0 or x >= self.size:

                        pass

                    elif y < 0 or y >= self.height:

                        pass

                    elif z < 0 or z >= self.size:

                        pass

                    else:

                        selected_blocks.append((x, y, z))

        for block in selected_blocks:

            if abs(block[0] + self.position.x - point.x) < 0.5:
                if abs(block[1] + self.position.y - point.y) < 0.5:
                    if abs(block[2] + self.position.z - point.z) < 0.5:

                        if self.blocks[block] is not None:

                            # print("Collision: {}".format(block))
                            # print(counter)

                            return True

            # counter += 1

        return False

        # if self.block_collision(point) != None:
        #
        #     return True
        #
        # else:
        #
        #     return False

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

    def __str__(self):
        """String representation of chunk."""

        return 'SmallChunk: ' + str(self.blocks)


class NormalChunk(Chunk):
    """Normal chunk of blocks - 8x8x128."""

    # size of chunk side
    size = 8
    # chunk height
    height = 128

    def __str__(self):
        """String representation of chunk."""

        return 'NormalChunk: ' + str(self.blocks)


class BlockWorld(object):
    """World encapsulates blocks in chunks."""

    def __init__(self, chunk_type, width, depth):

        self.chunk_type = chunk_type
        self.chunk_size = self.chunk_type.size
        self.chunk_offset = 0.5

        self.width = width
        self.depth = depth

        self.chunks = {}

        self.generate_world()

    def in_chunk(self, point):
        """Return chunk key according the point."""

        for position, chunk in self.chunks.items():

            x_dist = point.x - position[0] + self.chunk_offset
            z_dist = point.z - position[1] + self.chunk_offset
            if (0 < x_dist < chunk.size) and (0 < z_dist < chunk.size):

                return position

    def collision(self, point):
        """Return collision with world as a boolean.

        Args:
            point (Point): Check collision for the point.

        Returns:
            bool: Point collision with world.
        """

        point.z = -point.z

        offset = 0.5

        # counter = 0
        for chunk in self.chunks:

            if (chunk[0] < point.x + offset and
                            point.x - offset < chunk[0] + self.chunk_size):
                if (chunk[1] < point.z + offset and
                                point.z - offset < chunk[1] + self.chunk_size):

                    if self.chunks[chunk].collision(point):

                        # print(counter)
                        return True

            # counter += 1

        return False

    def __str__(self):
        """String representation for world."""

        return 'BlockWorld: ' + str(self.chunks)

    def generate_chunk(self, position):
        """Generate chunk.

        Args:
            position ((int, int)): Chunk position in world.
        """

        if not self.chunk_exists(position):

            # print("Creating new chunk: {}".format(position))

            self.chunks[position] = self.chunk_type(
                Point(position[0], 0, position[1]))

    def chunk_exists(self, position):
        """Return chunk existence on the position.

        Args:
            position ((int, int)): Chunk position.
        """

        return position in self.chunks

    def find_necessary_chunks(self, point, distance):
        """Find necessary chunks in the distance.

        Args:
            point (Point): centre point
            distance (int): distance

        Returns:
            list: list of necessary chunks positions
        """

        offset = self.chunk_size / 2

        min_x = int(point.x - distance) - offset
        min_z = int(point.z - distance) - offset
        max_x = int(point.x + distance) - offset
        max_z = int(point.z + distance) - offset

        positions = []
        for x_pos in range(min_x, max_x):
            for z_pos in range(min_z, max_z):

                if x_pos % self.chunk_size == 0 and z_pos % self.chunk_size == 0:

                    if sqrt(pow((x_pos + offset) - point.x, 2)
                            + pow((z_pos + offset) - point.z, 2)) > distance:

                        pass

                    else:

                        positions.append((x_pos, z_pos))

        return positions

    def find_nearest_chunks(self, point):

        return self.find_necessary_chunks(point, 7)

    def block_collision(self, point, chunks):

        for chunk in chunks:

            print(self.chunks[chunk].block_collision(point))

    def generate_chunks(self, point, distance):

        necessary_chunks = self.find_necessary_chunks(point, distance)

        for position in necessary_chunks:

            self.generate_chunk(position)

    def set_visibility(self, point, distance):
        """Set chunk visibility.

        Args:
            point (Point): Observer position.
            distance (int): Distance.
        """

        for position, chunk in self.chunks.items():

            if point.chunk_distance(chunk.get_centre()) > distance:

                chunk.visible = False

            else:

                chunk.visible = True

    def generate_world(self):
        """Generate world from chunks."""

        for x in range(0, self.width, self.chunk_size):
            for z in range(0, self.depth, self.chunk_size):

                # self.chunks[(x, z)] = self.chunk_type(Point(x, 0, z))
                self.generate_chunk((x, z))
