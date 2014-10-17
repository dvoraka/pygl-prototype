"""Module for graphic representation."""

from __future__ import print_function

import pyglet
import sys

from pyglet.window import key

# PyOpenGL imports
from OpenGL.GL import GL_ARRAY_BUFFER
from OpenGL.GL import GL_COLOR_BUFFER_BIT
from OpenGL.GL import GL_CULL_FACE
from OpenGL.GL import GL_DEPTH_BUFFER_BIT
from OpenGL.GL import GL_DEPTH_TEST
from OpenGL.GL import GL_FALSE
from OpenGL.GL import GL_FLOAT
from OpenGL.GL import GL_MODELVIEW
from OpenGL.GL import GL_PROJECTION
from OpenGL.GL import GL_STATIC_DRAW
from OpenGL.GL import GL_TRIANGLES

from OpenGL.GL import GLfloat
from OpenGL.GL import GLuint

from OpenGL.GL import glBindBuffer
from OpenGL.GL import glBufferData
from OpenGL.GL import glClear
from OpenGL.GL import glClearColor
from OpenGL.GL import glDisable
from OpenGL.GL import glDisableVertexAttribArray
from OpenGL.GL import glDrawArrays
from OpenGL.GL import glEnable
from OpenGL.GL import glEnableVertexAttribArray
from OpenGL.GL import glGenBuffers
from OpenGL.GL import glIsEnabled
from OpenGL.GL import glLoadIdentity
from OpenGL.GL import glMatrixMode
from OpenGL.GL import glOrtho
from OpenGL.GL import glRotatef
from OpenGL.GL import glTranslatef
from OpenGL.GL import glUseProgram
from OpenGL.GL import glVertexAttribPointer
from OpenGL.GL import glViewport

from OpenGL.GLU import gluPerspective

# project imports
import camera
import controls
import player
import script
import shaders


class TestObject(object):
    """Test rendering object."""

    def __init__(self):

        self.vbo = GLuint()

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

        glGenBuffers(1, self.vbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER,
            len(self.vertexes_GL) * 4,
            self.vertexes_GL,
            GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self):
        """Draw test object."""

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glDisableVertexAttribArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


class GraphicBlock(object):
    """Graphic data representation for block."""

    def __init__(self):

        pass

    @staticmethod
    def get_vertexes(position):
        """Return vertex list from position."""

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
        points[29] = (x_pos + 0.5, y_pos - 0.5, z_pos - 0.5)

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


class VboData(object):
    """VBO data structure."""

    def __init__(self, chunk_id):

        self.name = GLuint()
        glGenBuffers(1, self.name)

        self.chunk_id = chunk_id
        self.vertexes_count = 0

        # render flag
        self.render = False


class GameWindow(pyglet.window.Window):
    """Show game window."""

    def __init__(self, renderer):

        super(GameWindow, self).__init__()
        self.set_caption('GL prototype')

        self.renderer = renderer

        self.set_exclusive_mouse(True)

        # detect OpenGL capabilities
        self.capabilities = None
        self.detect_capabilities()

        if self.capabilities == "unsupported":

            print("Unsupported OpenGL version.")
            sys.exit()

        # schedule tasks
        pyglet.clock.schedule_interval(self.print_info, 4.0 / 1.0)
        pyglet.clock.schedule_interval(self.less_frequent_tasks, 1.0 / 2.0)
        pyglet.clock.schedule_interval(self.update, 1.0 / 30.0)

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        # camera settings
        self.camera = camera.FPSCamera(x_pos=10, y_pos=53, z_pos=-20)
        self.camera.set_gravity(True)
        self.camera_fall_collision = True

        self.devel_keys_enabled = True

        # script mode settings
        self.scripter = script.Script("script.txt", self.camera)
        if self.scripter:

            # self.camera.set_gravity(False)
            self.camera.set_gravity(True)

        # player's body
        self.player = player.PlayerBody(self.camera, self.renderer, 0.1, 1.9)

        # controller for player's input
        self.controller = controls.Controller(self.player, "settings.ini")

        #self.collision_offset = 0.1

        self.update_counter = 0

        self.test_label = pyglet.text.Label(
            'TEST Label',
            font_size=36,
            x=self.width / 2,
            y=self.height,
            anchor_x='center',
            anchor_y='top'
        )

        # init shaders
        shader_pool = shaders.ShaderPool(self.capabilities)
        self.shader_programs = shader_pool.get_shaders()

        # initial rendering - fill, lines, points
        self.rendering_type = "fill"

        # variables for scheduling
        self.long_tasks = 3
        self.long_tasks_counter = 0

        self.setup()

    @staticmethod
    def print_fps(dt):
        """Print FPS."""

        print(pyglet.clock.get_fps())

    def print_info(self, dt):
        """Print useful info."""

        print("FPS: {}".format(pyglet.clock.get_fps()))
        print(self.camera.get_position())

    def print_gl_info(self):
        """Print OpenGL info."""

        print("=" * 40)
        print("OpenGL info")
        print("renderer: {}".format(pyglet.gl.gl_info.get_renderer()))
        print("version: {}".format(pyglet.gl.gl_info.get_version()))
        print("capabilities: {}".format(self.capabilities))
        #print(self.config)
        print("+" * 40)
        print("")

    def print_gl_settings(self):
        """Print OpenGL settings."""

        print("=" * 40)
        print("OpenGL settings")
        print("Depth test: {}".format(glIsEnabled(GL_DEPTH_TEST)))
        print("Culling: {}".format(glIsEnabled(GL_CULL_FACE)))
        print("+" * 40)
        print("")

    def detect_capabilities(self):
        """Detect OpenGL capabilities."""

        if pyglet.gl.gl_info.have_version(3, 3):

            self.capabilities = "normal"

        elif pyglet.gl.gl_info.have_version(3, 1):

            self.capabilities = "old"

        elif pyglet.gl.gl_info.have_version(2, 1):

            self.capabilities = "legacy"

        else:

            self.capabilities = "unsupported"

    def setup(self):
        """Setup OpenGL."""

        self.print_gl_info()

        glClearColor(1.0, 1.0, 1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        self.print_gl_settings()

    def on_resize(self, width, height):
        """Prepare perspective for window size."""

        print('on resize')

        if height == 0:

            height = 1

        glViewport(0, 0, width, height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(75, 1.0 * width / height, 0.001, 1000.0)

    def show(self):
        """Show window and start app."""

        pyglet.app.run()

    def set_2d(self):
        """Set 2D render mode."""

        glDisable(GL_DEPTH_TEST)

        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        """Set 3D render mode."""

        glEnable(GL_DEPTH_TEST)

        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(75.0, 1.0 * self.width / self.height, 0.001, 1000.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def use_shader(self, shader_name):
        """Use cached shader.

        Args:
            shader_name (str): shader name in cache dict
        """

        if shader_name in self.shader_programs:

            glUseProgram(self.shader_programs[shader_name])

        else:

            glUseProgram(0)

    def on_draw(self):
        """Redraw window."""

        self.set_3d()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # rotate camera
        glRotatef(self.camera.v_angle_deg(), 1.0, 0, 0)
        glRotatef(self.camera.h_angle_deg(), 0.0, 1.0, 0)

        glTranslatef(
            -self.camera.x_pos,
            -self.camera.y_pos,
            self.camera.z_pos)

        if self.rendering_type == "fill":

            self.use_shader("test")

        elif self.rendering_type == "lines":

            self.use_shader("lines")

        self.renderer.render()

        # draw HUD
        self.set_2d()
        self.draw_hud()

    def draw_hud(self):
        """Render HUD."""

        #TODO: add resize changes
        # glUseProgram(self.hud_shader)
        # temporary solution
        glUseProgram(0)
        self.test_label.draw()

    def on_mouse_motion(self, x, y, dx, dy):

        self.camera.add_v_angle(float(dy))
        self.camera.add_h_angle(float(dx))

    def fill_rendering(self):
        """Set fill rendering option."""

        self.rendering_type = "fill"
        self.renderer.set_fill()

    def lines_rendering(self):
        """Set lines rendering option."""

        self.rendering_type = "lines"
        self.renderer.set_lines()

    def toggle_fullscreen(self):

        if self.fullscreen:

            self.set_fullscreen(False)
            self.set_exclusive_mouse(True)
            self.set_mouse_visible(False)

        else:

            self.set_fullscreen(True)
            self.set_exclusive_mouse(True)
            self.set_mouse_visible(False)

    def less_frequent_tasks(self, dt):

        if self.long_tasks_counter % self.long_tasks == 0:

            self.renderer.check_visibility(
                self.camera.get_position_inverse_z())
            self.renderer.set_visibility()

        elif self.long_tasks_counter % self.long_tasks == 1:

            self.renderer.prepare_new_chunks(
                self.camera.get_position_inverse_z())

        elif self.long_tasks_counter % self.long_tasks == 2:

            self.renderer.create_vbos()

        self.long_tasks_counter += 1

    def testing_zone(self):

        if self.update_counter % 120 == 0:

            print(self.renderer.world.in_chunk(
                self.camera.get_position_inverse_z()))

            cposition = self.camera.get_position_inverse_z()
            nchunks = self.renderer.world.find_nearest_chunks(cposition)
            # print(self.renderer.world.block_collision(cposition, nchunks))

        if self.scripter:

            self.scripter.next_action()

    def devel_keys(self):

        # toggle gravity
        if self.keyboard[key._7]:

            self.keyboard[key._7] = False
            if self.camera.gravity:

                self.camera.set_gravity(False)
                self.camera.stop_falling()

            else:

                self.camera.set_gravity(True)

        # move up
        if self.keyboard[key._8]:

            self.camera.up()

        # move down
        elif self.keyboard[key._9]:

            self.camera.down()

        # lines rendering
        if self.keyboard[key._2]:

            self.lines_rendering()

        # fill rendering
        elif self.keyboard[key._1]:

            self.fill_rendering()

        # points rendering in future

        # toggle fullscreen
        elif self.keyboard[key._6]:

            self.keyboard[key._6] = False

            self.toggle_fullscreen()

        # disable exclusive mouse
        elif self.keyboard[key.INSERT]:

            self.set_exclusive_mouse(False)

    def testing_keys(self):
        """Keys for testing and temporary purposes."""

        if self.keyboard[key.NUM_1]:

            self.camera.sprint()

        elif self.keyboard[key.NUM_2]:

            self.keyboard[key.NUM_2] = False
            self.scripter.stop()

        elif self.keyboard[key.NUM_3]:

            self.keyboard[key.NUM_3] = False
            self.scripter.start()

        # elif self.keyboard[key.SPACE]:
        #
        #     self.camera.jump()

        elif self.keyboard[key.R]:

            self.keyboard[key.R] = False
            self.scripter.reload("script.txt")

    def update(self, dt):

        self.testing_zone()

        # send keys status to controller
        self.controller.update(self.keyboard)

        # development keys
        if self.devel_keys_enabled:

            self.devel_keys()

        # testing keys
        self.testing_keys()

        self.update_counter += 1
