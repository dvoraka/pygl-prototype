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

from multiprocessing import Lock
from multiprocessing.sharedctypes import Array
from multiprocessing.sharedctypes import copy
from ctypes import c_float

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

# mpl = mp.log_to_stderr(5)

### multiprocessing infrastructure
####################################

lock = Lock()
size = 250000
shared_array = Array(c_float, size, lock=lock)


def long_func(chunk_data):

    print("{}, PID: {} ({})".format(
        "long_func", os.getpid(), os.getppid()))
    time.sleep(random.randint(1, 9))

    positions = generate_vbo_blocks(chunk_data)

    return chunk_data, positions


def gl_vertexes_mp(chunk_id, chunk_vertexes):
    """MP wrapper."""

    shared_array.get_lock().acquire()

    raw_array = shared_array.get_obj()

    index = 0
    for value in chunk_vertexes:

        raw_array[index] = value

        index += 1

    return chunk_id


def generate_gl_vertexes(chunk_vertexes):
    """Generate vertex data.

    Args:
        chunk_vertexes (list): vertexes of chunk
    """

    gl_vertexes = (GLfloat * len(chunk_vertexes))(*chunk_vertexes)

    return gl_vertexes


def vertexes_mp(chunk_id, positions):
    """MP wrapper."""

    vertexes = generate_vertexes(positions)

    return chunk_id, vertexes


def generate_vertexes(positions):

    vertexes = []
    for position in positions:

        vertexes.extend(graphics.GraphicBlock.get_vertexes(position))

    return vertexes


def positions_mp(chunk_data):
    """MP wrapper."""

    positions = generate_vbo_blocks(chunk_data)

    return chunk_data, positions


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

    positions = generate_vbo_blocks(chunk_data)

    chunk_vertexes = generate_vertexes(positions)

    gl_vertexes = generate_gl_vertexes(chunk_vertexes)

    chunk_vbo = graphics.VboData(chunk_data.chunk_id)
    chunk_vbo.vertexes_count = len(gl_vertexes)

    glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)
    glBufferData(
        GL_ARRAY_BUFFER,
        len(gl_vertexes) * 4,
        gl_vertexes,
        GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    return chunk_vbo


class VboCreator(object):
    """Create VBO data object."""

    def __init__(self, vbo_list, workers=2):

        self.orig_list = vbo_list

        self.active_tasks = []
        self.active_subtasks = {}

        self.prepared_vbos = {}

        self.ready_vbos = collections.deque()

        self.vbo_parts = {
            # "vbo_id": {
            #     "parts1": (1, 2,),
            #     "parts2": ("a", "b", "d"),
            #     "parts3": None,
            # },
        }

        self.pool = mp.Pool(workers)

    def add_task(self, chunk_id):

        log.debug("New VboCreator task: {}".format(chunk_id))

        self.active_tasks.append(chunk_id)

    def task_exists(self, chunk_id):

        if chunk_id in self.active_tasks:

            return True

        else:

            return False

    def create_subtasks(self, vbo_id):

        self.active_subtasks[vbo_id] = {
            "positions": None,
            "vertexes": None,
            "gl_vertexes": None,
        }

    def set_subtask_state(self, vbo_id, subtask, state):

        self.active_subtasks[vbo_id][subtask] = state

    def create_parts(self, vbo_id):

        self.vbo_parts[vbo_id] = {
            "positions": None,
            "vertexes": None,
            "gl_vertexes": None,
        }

    def delete_parts(self, vbo_id):

        del self.vbo_parts[vbo_id]

    def add_parts(self, vbo_id, section, data):

        self.vbo_parts[vbo_id][section] = data

    def add_ready_vbo(self, uid):

        self.ready_vbos.append(uid)

    def check_parts(self):

        log.debug("Active VboCreator tasks: {}".format(len(self.active_tasks)))

        for vbo_id, value in self.vbo_parts.items():

            all_parts = []
            for part_name, data in value.items():

                if data:

                    if (part_name == "positions"
                            and not self.active_subtasks[vbo_id]["vertexes"]):

                        positions = data
                        self.pool.apply_async(
                            vertexes_mp,
                            args=(vbo_id, positions),
                            callback=self.vertexes_done
                        )
                        self.set_subtask_state(vbo_id, "vertexes", "running")

                        all_parts.append(False)

                    elif (part_name == "vertexes"
                            and not self.active_subtasks[vbo_id]["gl_vertexes"]):

                        vertexes = data
                        self.pool.apply_async(
                            gl_vertexes_mp,
                            args=(vbo_id, vertexes),
                            callback=self.gl_vertexes_done
                        )
                        self.set_subtask_state(vbo_id, "gl_vertexes", "running")

                        all_parts.append(False)

                    else:

                        all_parts.append(True)

                else:

                    all_parts.append(False)

            # print(all_parts)
            if all(all_parts):

                if vbo_id not in self.ready_vbos:

                    self.add_ready_vbo(vbo_id)

    def create(self, chunk_data):

        chunk_id = chunk_data.chunk_id
        if self.task_exists(chunk_id):

            return

        self.add_task(chunk_id)
        self.create_subtasks(chunk_id)
        self.create_parts(chunk_id)

        self.pool.apply_async(
            positions_mp,
            args=(chunk_data,),
            callback=self.positions_done
        )
        self.set_subtask_state(chunk_id, "positions", "running")

    def build_ready_vbos(self):

        if len(self.ready_vbos) > 0:

            new_vbo = self.ready_vbos.popleft()

            self.build_vbo(
                new_vbo,
                self.vbo_parts[new_vbo]["vertexes"],
                self.vbo_parts[new_vbo]["gl_vertexes"],
            )

            self.delete_parts(new_vbo)

            log.debug("VboCreator task {} done.".format(new_vbo))

    def build_vbo(self, uid, vertexes, gl_vertexes):

        chunk_vertexes = vertexes
        gl_vertexes = gl_vertexes

        vertexes_count = len(chunk_vertexes)

        chunk_vbo = graphics.VboData(uid)
        chunk_vbo.vertexes_count = vertexes_count

        glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)
        glBufferData(
            GL_ARRAY_BUFFER,
            vertexes_count * 4,
            gl_vertexes,
            GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        self.active_tasks.remove(uid)
        self.orig_list.append(chunk_vbo)

    def wait_for_procs(self):

        self.pool.close()
        self.pool.join()

    def positions_done(self, arg):

        log.debug("positions done")

        chunk_data = arg[0]
        positions = arg[1]

        self.add_parts(chunk_data.chunk_id, "positions", positions)
        self.set_subtask_state(chunk_data.chunk_id, "positions", "done")

    def vertexes_done(self, arg):

        log.debug("vertexes done")

        uid = arg[0]
        vertexes = arg[1]

        self.add_parts(uid, "vertexes", vertexes)
        self.set_subtask_state(uid, "vertexes", "done")

    def gl_vertexes_done(self, arg):

        log.debug("gl_vertexes done")

        uid = arg
        c_array = copy(shared_array.get_obj())

        shared_array.get_lock().release()

        self.add_parts(uid, "gl_vertexes", c_array)
        self.set_subtask_state(uid, "gl_vertexes", "done")

    def update(self):

        self.check_parts()

        self.build_ready_vbos()


class Renderer(object):
    """Render world."""

    def __init__(self, world, configuration=None):

        log.debug("Renderer initializing...")

        self.world = world
        self.visibility = 22
        self.chunk_gen_distance = self.visibility * 1.2

        # VboData list for vertex buffer objects
        self.vbos = []

        self.vbo_creator = VboCreator(self.vbos, workers=2)

        # external configuration
        self.configuration = configuration.get_values()
        self.update_configuration()

        log.debug("Renderer initialized.")

    # def print_info(self, point):
    #     """Development info method."""
    #
    #     # print(self.world.find_necessary_chunks(point, 10))
    #     pass

    def update_configuration(self):
        """Update configuration of renderer."""

        if not self.configuration:
            return

        self.visibility = int(self.configuration["visibility"])

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

    def data_update(self):

        self.vbo_creator.update()
        self.world.update_chunks()

    def create_vbos(self):
        """Create necessary VBOs."""

        for position, chunk in self.world.chunks.items():

            if self.vbo_exists(chunk.chunk_id):

                pass

            else:

                self.vbo_creator.create(chunk)

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
