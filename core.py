"""Core graphics module."""

from __future__ import print_function

from OpenGL.GL import GLfloat
from OpenGL.GL import glBindBuffer
from OpenGL.GL import glBufferData
from OpenGL.GL import glEnableVertexAttribArray
from OpenGL.GL import glDisableVertexAttribArray
from OpenGL.GL import glVertexAttribPointer
from OpenGL.GL import glDrawArrays
from OpenGL.GL import glPolygonMode
from OpenGL.GL import glEnable
from OpenGL.GL import glDisable

from OpenGL.GL import GL_ARRAY_BUFFER
from OpenGL.GL import GL_STATIC_DRAW
from OpenGL.GL import GL_FLOAT
from OpenGL.GL import GL_FALSE
from OpenGL.GL import GL_TRIANGLES
from OpenGL.GL import GL_CULL_FACE
from OpenGL.GL import GL_FRONT_AND_BACK
from OpenGL.GL import GL_LINE
from OpenGL.GL import GL_FILL
from OpenGL.GL import GL_POINTS

import collections
import multiprocessing as mp
import time

import graphics

from decorators import print_time


### multiprocessing infrastructure
####################################

vbos_queue = collections.deque()

# {'uid': list}
is_done = {}

#TODO: define structures for object parts
# queue1
# queue2
# ...


def vbo_done(vbo_data):
    """Testing callback."""

    vbos_queue.append(vbo_data)
    print("vbo done")


def add_vbo(vbo):
    """Add new VBO to queue/list."""

    # add vbo to vbos_queue
    pass


def build_vbo():
    """Build final VBO object."""

    # call add_vbo with result
    pass


def generate_vbo_async(chunk_data):
    """Asynchronous variant for VBO generation."""

    pass


@print_time
def generate_vertexes(chunk_vertexes):
    """Generate vertex data.

    Args:
        chunk_vertexes (list): vertexes of chunk
    """

    vertexes = (GLfloat * len(chunk_vertexes))(*chunk_vertexes)

    return vertexes


def generate_vbo_blocks(chunk_data):
    """Generate blocks data.

    Args:
        chunk_data (Chunk): chunk data
    """

    blocks_positions = []
    for rel_pos, block in chunk_data.blocks.items():

        block_position = (
            chunk_data.position.x + rel_pos[0],
            rel_pos[1],
            chunk_data.position.z + rel_pos[2]
        )

        if block is not None:

            blocks_positions.append(block_position)

    return blocks_positions

###### MP end
######################################


def generate_vbo(chunk_data):
    """Generate VBO object.

    Args:
        chunk_data (Chunk): chunk data

    Return:
        VboData: VBO data object
    """

    chunk_vbo = graphics.VboData(chunk_data.chunk_id)

    blocks_positions = generate_vbo_blocks(chunk_data)
    chunk_vertexes = []
    for position in blocks_positions:

        chunk_vertexes.extend(graphics.GraphicBlock.get_vertexes(position))

    vertexes_GL = generate_vertexes(chunk_vertexes)

    chunk_vbo.vertexes_count = len(vertexes_GL)

    glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)
    glBufferData(
        GL_ARRAY_BUFFER,
        len(vertexes_GL) * 4,
        vertexes_GL,
        GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return chunk_vbo


class VboCreator(object):
    """Create VBO data object."""

    def __init__(self, vbo_list):

        self.orig_list = vbo_list

        self.active_tasks = []
        self.pool = mp.Pool(4)

    def create(self, chunk_data):

        if chunk_data.chunk_id in self.active_tasks:

            print("task already exists")
            return

        self.active_tasks.append(chunk_data.chunk_id)


class Renderer(object):
    """Render world."""

    def __init__(self, world):

        self.world = world
        self.visibility = 17
        self.chunk_gen_distance = self.visibility * 1.1

        # VboData list for vertex buffer objects
        self.vbos = []

        self.pool = mp.Pool(2)

    def print_info(self, point):
        """Development info method."""

        # print(self.world.find_necessary_chunks(point, 10))
        pass

    def ground_collision(self, point):
        """Return ground collision value as boolean.

        Args:
            point (Point): Point for collision check.

        Return:
            boolean
        """

        return self.world.collision(point)

    def prepare_new_chunks(self, position):
        """Generate new chunks around the position.

        Args:
            position (Point): Centre.
        """

        self.world.generate_chunks(position, self.chunk_gen_distance)

    def print_visibility(self):
        """Print visibility for all chunks in world."""

        for position, chunk in self.world.chunks.items():

            print(position, chunk.visible)

    def check_visibility(self, point):
        """Check and set visibility for chunks.

        Args:
            point (Point): Centre.
        """

        self.world.set_visibility(point, self.visibility)

    def set_visibility(self):
        """Set visibility for VBOs according to world data."""

        for position, chunk in self.world.chunks.items():

            for vbo in self.vbos:

                if vbo.chunk_id == chunk.chunk_id:

                    vbo.render = chunk.visible

    def create_vbos(self):
        """Create necessary VBOs."""

        for position, chunk in self.world.chunks.items():

            if self.vbo_exists(chunk.chunk_id):

                pass

            else:

                new_vbo = generate_vbo(chunk)
                self.vbos.append(new_vbo)

                # self.prepare_vbo(chunk)

    def vbo_exists(self, chunk_id):
        """Check VBO existence for the chunk ID.

        Args:
            chunk_id (str): Chunk ID.

        Return:
            boolean: True if VBO data exists.
        """

        for vbo in self.vbos:

            if vbo.chunk_id == chunk_id:

                return True

        return False

    # @staticmethod
    # @print_time
    # def generate_vbo(chunk_data):
    #     """Generate VBO object.
    #
    #     Args:
    #         chunk_data (Chunk): Chunk data.
    #
    #     Return:
    #         VboData: VBO data object.
    #     """
    #
    #     # print("Generating VBO...")
    #
    #     blocks_positions = []
    #
    #     chunk_vbo = graphics.VboData(chunk_data.chunk_id)
    #     glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)
    #
    #     for rel_pos, block in chunk_data.blocks.items():
    #
    #         block_position = (
    #             chunk_data.position.x + rel_pos[0],
    #             rel_pos[1],
    #             chunk_data.position.z + rel_pos[2]
    #         )
    #
    #         if block is not None:
    #
    #             blocks_positions.append(block_position)
    #
    #     chunk_vertexes = []
    #     for position in blocks_positions:
    #
    #         chunk_vertexes.extend(graphics.GraphicBlock.get_vertexes(position))
    #
    #     vertexes_GL = (GLfloat * len(chunk_vertexes))(*chunk_vertexes)
    #
    #     chunk_vbo.vertexes_count = len(vertexes_GL)
    #
    #     glBufferData(
    #         GL_ARRAY_BUFFER,
    #         len(vertexes_GL) * 4,
    #         vertexes_GL,
    #         GL_STATIC_DRAW)
    #     glBindBuffer(GL_ARRAY_BUFFER, 0)
    #
    #     return chunk_vbo

    # @staticmethod
    # def generate_vbo(chunk_data):
    #
    #     return generate_vbo(chunk_data)

    def prepare_vbo(self, chunk_data):

        self.pool.apply_async(
            generate_vbo, args=(chunk_data,), callback=vbo_done)

    def get_new_vbo(self):

        if len(vbos_queue) > 0:

            return vbos_queue.popleft()

    def check_new_vbo(self):

        new_vbo = self.get_new_vbo()

        print(new_vbo)

        if new_vbo:

            self.vbos.append(new_vbo)
            print(len(self.vbos))

    def prepare_world(self):
        """Fill buffer objects with data."""

        block_counter = 0
        for pos, chunk in self.world.chunks.items():

            # b_positions = []
            #
            # chunk_vbo = graphics.VboData(chunk.chunk_id)
            # glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)
            #
            # for rel_pos, block in chunk.blocks.items():
            #
            #     block_position = (
            #         pos[0] + rel_pos[0],
            #         rel_pos[1],
            #         pos[1] + rel_pos[2]
            #     )
            #
            #     if block is not None:
            #
            #         b_positions.append(block_position)
            #         block_counter += 1
            #
            # chunk_vertexes = []
            # for position in b_positions:
            #
            #     chunk_vertexes.extend(
            #           graphics.GraphicBlock().get_vertexes(position))
            #
            # vertexes_GL = (GLfloat * len(chunk_vertexes))(*chunk_vertexes)
            #
            # chunk_vbo.vertexes_count = len(vertexes_GL)
            #
            # glBufferData(
            #     GL_ARRAY_BUFFER,
            #     len(vertexes_GL) * 4,
            #     vertexes_GL,
            #     GL_STATIC_DRAW)
            # glBindBuffer(GL_ARRAY_BUFFER, 0)

            chunk_vbo = generate_vbo(chunk)

            self.vbos.append(chunk_vbo)

        print("=" * 40)
        print("World info")
        print("Chunks: {}".format(len(self.vbos)))
        print("Blocks: {}".format(
            len(self.vbos) *
            self.world.chunk_type.size *
            self.world.chunk_type.size *
            self.world.chunk_type.height))
        print("Rendered blocks: {}".format(block_counter))
        print("+" * 40)
        print("")

    def render(self):
        """Render game world."""

        for vbo in self.vbos:

            if vbo.render:

                glBindBuffer(GL_ARRAY_BUFFER, vbo.name)
                glEnableVertexAttribArray(0)
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

                glDrawArrays(
                    GL_TRIANGLES,
                    0,
                    vbo.vertexes_count)
                glDisableVertexAttribArray(0)
                glBindBuffer(GL_ARRAY_BUFFER, 0)

    @staticmethod
    def set_lines():
        """Set OpenGL lines rendering."""

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDisable(GL_CULL_FACE)

    @staticmethod
    def set_fill():
        """Set OpenGL fill rendering."""

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_CULL_FACE)

    @staticmethod
    def set_points():
        """Set OpenGL points rendering."""

        glPolygonMode(GL_FRONT_AND_BACK, GL_POINTS)
