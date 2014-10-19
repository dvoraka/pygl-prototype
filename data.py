# -*- coding: utf-8 -*-
#

"""Module for data representation."""

import uuid
import collections
import logging
import multiprocessing as mp

from math import sqrt

from decorators import print_time
from functions import generate_chunk
from functions import generate_chunk_mp


log = logging.getLogger(__name__)


class ChunkCreator(object):

    def __init__(self, chunk_dict, workers=2):

        self.orig_dict = chunk_dict

        self.active_tasks = []
        # self.prepared_chunks = {}
        self.ready_chunks = collections.deque()

        self.pool = mp.Pool(workers)

    def add_task(self, chunk_position):

        log.debug("New ChunkCreator task: {}".format(chunk_position))

        self.active_tasks.append(chunk_position)

    def task_exists(self, position):

        if position in self.active_tasks:

            return True

        else:

            return False

    def add_ready_chunk(self, position):

        self.ready_chunks.append(position)

    def create(self, chunk_type, chunk_position):

        width = chunk_type.size
        height = chunk_type.height

        if self.task_exists(chunk_position):

            return

        print("add task: {}".format(chunk_position))
        self.add_task(chunk_position)

        self.pool.apply_async(
            generate_chunk_mp,
            args=(width, height),
            callback=self.chunk_done
        )

    def build_ready_chunks(self):

        if len(self.ready_chunks) > 0:

            new_chunk = self.ready_chunks.popleft()

            self.build_chunk()

            log.debug("ChunkCreator task {} done.".format(new_chunk))

    def build_chunk(self, position):

        new_chunk = None

        self.active_tasks.remove(position)
        self.orig_dict.append(new_chunk)

    def chunk_done(self, arg):

        print("chunk done")

    def update(self):

        self.build_ready_chunks()

    def wait_for_procs(self):

        self.pool.close()
        self.pool.join()


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

    def __eq__(self, other):

        if not isinstance(other, Point):

            return False

        if self.x == other.x and self.y == other.y and self.z == other.z:

            return True

    def __ne__(self, other):

        return not self == other

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

        blocks = generate_chunk(self.size, self.height)

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
        """Return boolean value of collision for the point.

        Args:
            point (Point): check collision for this point
        """

        # debug info
        # counter = 0

        # list of (x, y, z) of int
        selected_blocks = []
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
    """Small chunk - 2 x 2 x 128 blocks."""

    # size of chunk side
    size = 2
    # height of chunk
    height = 128

    def __str__(self):
        """String representation of chunk."""

        return 'SmallChunk: ' + str(self.blocks)


class NormalChunk(Chunk):
    """Normal chunk - 8 x 8 x 128 blocks."""

    # size of chunk side
    size = 8
    # height of chunk
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
        """Return chunk key according the point.

        Args:
            point (Point): find chunk including this point
        """

        for position, chunk in self.chunks.items():

            x_dist = point.x - position[0] + self.chunk_offset
            z_dist = point.z - position[1] + self.chunk_offset
            if (0 < x_dist < chunk.size) and (0 < z_dist < chunk.size):

                return position

    def collision(self, point):
        """Return collision with a world as a boolean.

        Args:
            point (Point): check collision for the point

        Return:
            bool: point collision with the world
        """

        # temporary solution
        #TODO: change
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

        return "BlockWorld: {} chunks".format(len(self.chunks))

    def generate_chunk(self, position):
        """Generate chunk.

        Args:
            position ((int, int)): position of chunk in a world
        """

        if not self.chunk_exists(position):

            # print("Creating new chunk: {}".format(position))

            # create chunk with creator

            self.chunks[position] = self.chunk_type(
                Point(position[0], 0, position[1]))

    def chunk_exists(self, position):
        """Return chunk existence on the position.

        Args:
            position ((int, int)): chunk position/key (x, z)
        """

        return position in self.chunks

    def find_necessary_chunks(self, point, distance):
        """Find necessary chunks in the distance.

        Args:
            point (Point): centre point
            distance (int): distance

        Return:
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

                if (x_pos % self.chunk_size == 0 and
                        z_pos % self.chunk_size == 0):

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
        """Set chunks visibility.

        Args:
            point (Point): observer position
            distance (int): max distance
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
