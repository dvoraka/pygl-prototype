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
import logging
import os
import pprint
import random

import graphics

from decorators import print_time
from decorators import print_pid


log = logging.getLogger(__name__)

### multiprocessing infrastructure
####################################


def long_func(chunk_data):

    # print("{}, PID: {} ({})".format(
    #     "long_func", os.getpid(), os.getppid()))
    # time.sleep(random.randint(1, 9))

    positions = generate_vbo_blocks(chunk_data)

    return (chunk_data, positions)


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

    blocks_positions = generate_vbo_blocks(chunk_data)
    chunk_vertexes = []
    for position in blocks_positions:

        chunk_vertexes.extend(graphics.GraphicBlock.get_vertexes(position))

    vertexes_gl = generate_vertexes(chunk_vertexes)

    chunk_vbo = graphics.VboData(chunk_data.chunk_id)
    chunk_vbo.vertexes_count = len(vertexes_gl)

    glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)
    glBufferData(
        GL_ARRAY_BUFFER,
        len(vertexes_gl) * 4,
        vertexes_gl,
        GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return chunk_vbo


class VboCreator(object):
    """Create VBO data object."""

    def __init__(self, vbo_list):

        self.orig_list = vbo_list

        self.active_tasks = []
        self.active_subtasks = {}

        self.prepared_vbos = {}

        self.ready_vbos = []

        self.vbo_parts = {
            "vbo_id": {
                "parts1": (1, 2,),
                "parts2": ("a", "b", "d"),
                "parts3": None,
            },
        }

        self.pool = mp.Pool(16)

    def add_task(self, chunk_id):

        # print("New task: {}".format(chunk_id))
        self.active_tasks.append(chunk_id)

    def task_exists(self, chunk_id):

        if chunk_id in self.active_tasks:

            return True

        else:

            return False

    def create_parts(self, vbo_id):

        self.vbo_parts[vbo_id] = {
            "positions": None
        }

    def delete_parts(self, vbo_id):

        del self.vbo_parts[vbo_id]

    def add_parts(self, vbo_id, section, data):

        self.vbo_parts[vbo_id][section] = data

    def add_ready_vbo(self, uid):

        self.ready_vbos.append(uid)

    def check_parts(self):

        print("Active tasks: {}".format(len(self.active_tasks)))

        for key, value in self.vbo_parts.items():

            all_parts = []
            for part_name, data in value.items():

                if data:

                    all_parts.append(True)

                else:

                    all_parts.append(False)

            if all(all_parts):

                if key not in self.ready_vbos:

                    self.add_ready_vbo(key)

    # @print_pid
    def create(self, chunk_data):

        chunk_id = chunk_data.chunk_id
        if self.task_exists(chunk_id):

            return

        self.add_task(chunk_id)
        # self.create_subtasks()
        self.create_parts(chunk_id)

        self.pool.apply_async(
            long_func, args=(chunk_data,), callback=self.positions_done)

    def build_ready_vbos(self):

        # test solution (slow)
        new_vbo = None
        if len(self.ready_vbos) > 0:

            new_vbo = self.ready_vbos.pop()

            self.build_vbo(new_vbo, self.vbo_parts[new_vbo]["positions"])
            self.delete_parts(new_vbo)

    def build_vbo(self, uid, positions):

        blocks_positions = positions  # generate_vbo_blocks(chunk_data)
        chunk_vertexes = []
        for position in blocks_positions:

            chunk_vertexes.extend(graphics.GraphicBlock.get_vertexes(position))

        vertexes_gl = generate_vertexes(chunk_vertexes)

        chunk_vbo = graphics.VboData(uid)
        chunk_vbo.vertexes_count = len(vertexes_gl)

        glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)
        glBufferData(
            GL_ARRAY_BUFFER,
            len(vertexes_gl) * 4,
            vertexes_gl,
            GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.active_tasks.remove(uid)
        self.orig_list.append(chunk_vbo)

    def wait_for_procs(self):

        self.pool.close()
        self.pool.join()

    def test_done1(self, arg):

        print("done1: {}".format(arg))

    def test_done2(self, arg):

        print("done2: {}".format(arg))

    def positions_done(self, arg):

        self.add_parts(arg[0].chunk_id, "positions", arg[1])


class Renderer(object):
    """Render world."""

    def __init__(self, world):

        log.debug("Renderer initializing...")

        self.world = world
        self.visibility = 18
        self.chunk_gen_distance = self.visibility * 1.2

        # VboData list for vertex buffer objects
        self.vbos = []

        # self.pool = mp.Pool(2)

        self.vbo_creator = VboCreator(self.vbos)

        log.debug("Renderer initialized.")

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

                self.vbo_creator.create(chunk)

                # self.vbo_creator.check_parts()
                # self.vbo_creator.build_ready_vbos()

                # new_vbo = generate_vbo(chunk)
                # self.vbos.append(new_vbo)

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

    def prepare_world(self):
        """Fill buffer objects with data."""

        block_counter = 0
        for pos, chunk in self.world.chunks.items():

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
