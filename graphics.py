'''Module for graphic representation.'''

import pyglet

#from OpenGL.GL import * # Some pyopengl problems
from pyglet.gl import *

from pyglet.window import key

import math

import shaders
import camera


class TestObject():
    '''Test rendering object.'''

    def __init__(self):

        self.bo = GLuint()

        self.vertexes = (
            0, 0, 0,
            1.0, 0, 0,
            1.0, 1.0, 0,
            0, 0, 0,
            1.0, 1.0, 0,
            0, 1.0, 0,
        )

        self.vertexes_GL = (GLfloat * len(
            self.vertexes))(*self.vertexes)

        glGenBuffers(1, self.bo)
        glBindBuffer(GL_ARRAY_BUFFER, self.bo)
        glBufferData(
            GL_ARRAY_BUFFER,
            len(self.vertexes_GL) * 4,
            self.vertexes_GL,
            GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self):
        
        glBindBuffer(GL_ARRAY_BUFFER, self.bo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class GraphicBlock:
    '''Graphic data representation for block.'''
    
    def __init__(self):
        
        pass

    def get_vertexes(self, position):
        '''Return vertex list from position.'''

        vertexes = []
        x_pos = float(position[0])
        y_pos = float(position[1])
        z_pos = float(position[2])

        points = 36 * [None]

        # front
        points[0] = (x_pos - 0.5, y_pos - 0.5, z_pos + 0.5)
        points[1] = (x_pos + 0.5, y_pos - 0.5, z_pos + 0.5)
        points[2] = (x_pos + 0.5, y_pos + 0.5, z_pos + 0.5)
        points[3] = (x_pos - 0.5, y_pos - 0.5, z_pos + 0.5)
        points[4] = (x_pos + 0.5, y_pos + 0.5, z_pos + 0.5)
        points[5] = (x_pos - 0.5, y_pos + 0.5, z_pos + 0.5)

        # top
        points[6] = (x_pos - 0.5, y_pos + 0.5, z_pos + 0.5)
        points[7] = (x_pos + 0.5, y_pos + 0.5, z_pos + 0.5)
        points[8] = (x_pos + 0.5, y_pos + 0.5, z_pos - 0.5)
        points[9] = (x_pos - 0.5, y_pos + 0.5, z_pos + 0.5)
        points[10] = (x_pos + 0.5, y_pos + 0.5, z_pos - 0.5)
        points[11] = (x_pos - 0.5, y_pos + 0.5, z_pos - 0.5)

        # right
        points[12] = (x_pos + 0.5, y_pos - 0.5, z_pos + 0.5)
        points[13] = (x_pos + 0.5, y_pos - 0.5, z_pos - 0.5)
        points[14] = (x_pos + 0.5, y_pos + 0.5, z_pos - 0.5)
        points[15] = (x_pos + 0.5, y_pos - 0.5, z_pos + 0.5)
        points[16] = (x_pos + 0.5, y_pos + 0.5, z_pos - 0.5)
        points[17] = (x_pos + 0.5, y_pos + 0.5, z_pos + 0.5)

        # left
        points[18] = (x_pos - 0.5, y_pos - 0.5, z_pos + 0.5)
        points[19] = (x_pos - 0.5, y_pos + 0.5, z_pos - 0.5)
        points[20] = (x_pos - 0.5, y_pos - 0.5, z_pos - 0.5)
        points[21] = (x_pos - 0.5, y_pos - 0.5, z_pos + 0.5)
        points[22] = (x_pos - 0.5, y_pos + 0.5, z_pos + 0.5)
        points[23] = (x_pos - 0.5, y_pos + 0.5, z_pos - 0.5)

        # back
        points[24] = (x_pos - 0.5, y_pos - 0.5, z_pos - 0.5)
        points[25] = (x_pos - 0.5, y_pos + 0.5, z_pos - 0.5)
        points[26] = (x_pos + 0.5, y_pos + 0.5, z_pos - 0.5)
        points[27] = (x_pos - 0.5, y_pos - 0.5, z_pos - 0.5)
        points[28] = (x_pos + 0.5, y_pos + 0.5, z_pos - 0.5)
        points[29] = (x_pos + 0.5, y_pos + 0.5, z_pos - 0.5)

        # bottom
        points[30] = (x_pos - 0.5, y_pos - 0.5, z_pos + 0.5)
        points[31] = (x_pos + 0.5, y_pos - 0.5, z_pos - 0.5)
        points[32] = (x_pos + 0.5, y_pos - 0.5, z_pos + 0.5)
        points[33] = (x_pos - 0.5, y_pos - 0.5, z_pos + 0.5)
        points[34] = (x_pos - 0.5, y_pos - 0.5, z_pos - 0.5)
        points[35] = (x_pos + 0.5, y_pos - 0.5, z_pos - 0.5)

        for point in points:

            vertexes.extend(point)

        return vertexes


class Renderer:
    '''Render world.'''

    def __init__(self, world):
        
        self.world = world
        # GLuint list for vertex buffer objects
        self.vbos = []
        self.vbos_vert_count = {}

    def prepare_world(self):
        '''Fill buffer objects with data.'''
        
        for pos, chunk in self.world.chunks.items():

            b_positions = []
            chunk_vertexes = []

            chunk_vbo = GLuint()
            glGenBuffers(1, chunk_vbo)
            glBindBuffer(GL_ARRAY_BUFFER, chunk_vbo)

            for rel_pos, block in chunk.blocks.items():

                block_position = (
                    pos[0] + rel_pos[0],
                    rel_pos[1],
                    pos[1] + rel_pos[2]
                )

                if block is not None:

                    b_positions.append(block_position)

            chunk_vertexes = []

            for position in b_positions:

                chunk_vertexes.extend(GraphicBlock().get_vertexes(position))

            vertexes_GL = (GLfloat * len(chunk_vertexes))(*chunk_vertexes)

            self.vbos_vert_count[chunk_vbo.value] = len(vertexes_GL)

            #print(len(vertexes_GL))

            glBufferData(
                GL_ARRAY_BUFFER,
                len(vertexes_GL) * 4,
                vertexes_GL,
                GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

            self.vbos.append(chunk_vbo)

        print('Chunks: {}'.format(len(self.vbos)))
        print('Blocks: {}'.format(
            len(self.vbos) *
            self.world.chunk_type.size *
            self.world.chunk_type.size *
            self.world.chunk_type.height))

    def render(self):
        
        for vbo in self.vbos:

            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
            # block count * vertex parts * vertex count
#            glDrawArrays(GL_TRIANGLES, 0,
#                self.world.chunk_type.size *
#                self.world.chunk_type.size *
#                self.world.chunk_type.height *
#                3 * 36)
            glDrawArrays(
                GL_TRIANGLES,
                0,
                self.vbos_vert_count[vbo.value])
            glDisableVertexAttribArray(0)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_lines(self):
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def set_fill(self):
        
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def set_points(self):

        glPolygonMode(GL_FRONT_AND_BACK, GL_POINTS)


class GameWindow(pyglet.window.Window):
    '''Show game window.'''

    def __init__(self, renderer):
        
        super(GameWindow, self).__init__()
        self.set_caption('GL prototype')

        #print(self.config)
        #self.set_fullscreen(True)

        pyglet.clock.schedule_interval(self.print_fps, 2.0 / 1.0)
        pyglet.clock.schedule_interval(self.update, 1.0 / 30.0)

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        self.renderer = renderer

        self.camera = camera.FPSCamera(x_pos=10, y_pos=53, z_pos=-20)

        # for testing only
        self.test_obj = TestObject()
        
        self.setup()

    def print_fps(self, dt):
        
        print(pyglet.clock.get_fps())

    def setup(self):
        '''Setup OpenGL.'''

        glClearColor(1.0, 1.0, 1.0, 0.0)

        # performance tests
        #glEnable(GL_CULL_FACE)
        #glCullFace(GL_BACK)
        #glFrontFace(GL_CCW)

        #glEnable(GL_DEPTH_TEST)
        ######################################

        self.renderer.set_lines()

        self.init_test_shader()

    def init_test_shader(self):
        '''Compile and use test shader.'''

        v_shader = shaders.load_vshader('shaders_data/simple.vs')
        f_shader = shaders.load_fshader('shaders_data/red.fs')

        program = shaders.compileProg(v_shader, f_shader)

        glUseProgram(program)

    def on_resize(self, width, height):
        '''Prepare perspective for window size.'''
        
        print('on resize')

        if height == 0:

            height = 1

        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(75, 1.0 * width / height, 0.001, 1000.0)

    def show(self):
        '''Show window and start app.'''
        
        pyglet.app.run()

    def on_draw(self):
        '''Redraw window.'''

        self.clear()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # rotate camera - temporary
        glRotatef((self.camera.v_angle * 180) / math.pi, 0.0, 1.0, 0)

        glTranslatef(
            -self.camera.x_pos,
            -self.camera.y_pos,
            self.camera.z_pos)

        self.test_obj.draw()
        self.renderer.render()

    def update(self, dt):
        
        if self.keyboard[key.UP]:

            self.camera.forward()

        elif self.keyboard[key.DOWN]:
            
            self.camera.backward()
         
        if self.keyboard[key.PAGEUP]:

            self.camera.up()

        elif self.keyboard[key.PAGEDOWN]:
            
            self.camera.down()
        
        if self.keyboard[key.LEFT]:

            self.camera.left()

        elif self.keyboard[key.RIGHT]:
            
            self.camera.right()

        if self.keyboard[key.L]:

            self.renderer.set_lines()

        elif self.keyboard[key.F]:
            
            self.renderer.set_fill()
