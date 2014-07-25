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

        # VboData list for vertex buffer objects
        self.vbos = []

    def ground_collision(self, point):
        """Return ground collision value as bool."""

        return self.world.collision(point)

    def print_visibility(self):

        for position, chunk in self.world.chunks.items():

            print(position, chunk.visible)

    def check_visibility(self, point):
        """Check and set visibility for chunks."""

        for position, chunk in self.world.chunks.items():

            #print(point.chunk_distance(chunk.get_centre()))
            if (point.chunk_distance(chunk.get_centre()) > self.visibility):

                # print(position)
                chunk.visible = False

            else:

                chunk.visible = True

    def prepare_world(self):
        """Fill buffer objects with data."""

        block_counter = 0
        for pos, chunk in self.world.chunks.items():

            b_positions = []

            chunk_vbo = graphics.VboData(chunk.chunk_id)
            glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo.name)

            for rel_pos, block in chunk.blocks.items():

                block_position = (
                    pos[0] + rel_pos[0],
                    rel_pos[1],
                    pos[1] + rel_pos[2]
                )

                if block is not None:

                    b_positions.append(block_position)
                    block_counter += 1

            chunk_vertexes = []
            for position in b_positions:

                chunk_vertexes.extend(graphics.GraphicBlock().get_vertexes(position))

            vertexes_GL = (GLfloat * len(chunk_vertexes))(*chunk_vertexes)

            chunk_vbo.vertexes_count = len(vertexes_GL)

            glBufferData(
                GL_ARRAY_BUFFER,
                len(vertexes_GL) * 4,
                vertexes_GL,
                GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

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

            skip_vbo = False
            for chunk in self.world.chunks.values():

                if vbo.chunk_id == chunk.chunk_id:

                    if not chunk.visible:

                        skip_vbo = True

            if skip_vbo:

                pass

            else:

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