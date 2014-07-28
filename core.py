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

import graphics


class Renderer(object):
    """Render world."""

    def __init__(self, world):

        self.world = world
        self.visibility = 20
        self.chunk_gen_distance = self.visibility * 1.1

        # VboData list for vertex buffer objects
        self.vbos = []

    def print_info(self, point):
        """Development info method."""

        # print(self.world.find_necessary_chunks(point, 10))
        pass

    def ground_collision(self, point):
        """Return ground collision value as bool."""

        return self.world.collision(point)

    def prepare_new_chunks(self, position):

        self.world.generate_chunks(position, self.chunk_gen_distance)

    def print_visibility(self):

        for position, chunk in self.world.chunks.items():

            print(position, chunk.visible)

    def check_visibility(self, point):
        """Check and set visibility for chunks."""

        self.world.set_visibility(point, self.visibility)

    def set_visibility(self):

        for position, chunk in self.world.chunks.items():

            for vbo in self.vbos:

                if vbo.chunk_id == chunk.chunk_id:

                    vbo.render = chunk.visible

    def create_vbos(self):

        for position, chunk in self.world.chunks.items():

            if self.vbo_exists(chunk.chunk_id):

                pass

            else:

                new_vbo = self.generate_vbo(chunk)
                self.vbos.append(new_vbo)

    def vbo_exists(self, chunk_id):

        for vbo in self.vbos:

            if vbo.chunk_id == chunk_id:

                return True

        return False

    def generate_vbo(self, chunk_data):

        blocks_positions = []

        chunk_vbo = graphics.VboData(chunk_data.chunk_id)
        glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)

        for rel_pos, block in chunk_data.blocks.items():

            block_position = (
                chunk_data.position.x + rel_pos[0],
                rel_pos[1],
                chunk_data.position.z + rel_pos[2]
            )

            if block is not None:

                blocks_positions.append(block_position)

        chunk_vertexes = []
        for position in blocks_positions:

            chunk_vertexes.extend(graphics.GraphicBlock().get_vertexes(position))

        vertexes_GL = (GLfloat * len(chunk_vertexes))(*chunk_vertexes)

        chunk_vbo.vertexes_count = len(vertexes_GL)

        glBufferData(
            GL_ARRAY_BUFFER,
            len(vertexes_GL) * 4,
            vertexes_GL,
            GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        return chunk_vbo

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
            #     chunk_vertexes.extend(graphics.GraphicBlock().get_vertexes(position))
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

            chunk_vbo = self.generate_vbo(chunk)

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

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glDisable(GL_CULL_FACE)

    @staticmethod
    def set_fill():

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glEnable(GL_CULL_FACE)

    @staticmethod
    def set_points():

        glPolygonMode(GL_FRONT_AND_BACK, GL_POINTS)