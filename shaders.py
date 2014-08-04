# -*- coding: utf-8 -*-
#

"""Module for shaders."""


# PyOpenGL imports
from OpenGL.GL import GL_VERTEX_SHADER
from OpenGL.GL import GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileShader
from OpenGL.GL.shaders import compileProgram


def read_shader(filename):
    """Read shader program from file and return it as a string."""

    with open(filename) as fh:

        shader = []
        for line in fh:

            shader.append(line)

    return "".join(shader)


def load_vshader(filename):
    """Return compiled vertex shader."""

    shader = read_shader(filename)
    vshader = compileShader(shader, GL_VERTEX_SHADER)

    return vshader


def load_fshader(filename):
    """Return compiled fragment shader."""

    shader = read_shader(filename)
    fshader = compileShader(shader, GL_FRAGMENT_SHADER)

    return fshader


def compile_program(*shaders):
    """Return compiled shader program."""

    return compileProgram(*shaders)


class ShaderPool(object):
    """Shader programs manager."""

    def __init__(self, capabilities):

        self.pool = {}
        self.capabilities = capabilities

        inits = {
            "legacy": self.init_legacy,
        }

        if capabilities in inits:

            inits[capabilities]()

        else:

            inits["legacy"]()

    def get_shaders(self):

        return self.pool

    def capabilities(self):

        return self.capabilities

    def init_legacy(self):

        self.pool["test"] = self.init_test_shader()
        self.pool["hud"] = self.init_hud_shader()
        self.pool["lines"] = self.init_line_shader()

    def init_test_shader(self):
        """Return compiled test shader."""

        v_shader = load_vshader('shaders_data/simple.vs')
        f_shader = load_fshader('shaders_data/test1.fs')

        program = compile_program(v_shader, f_shader)

        return program

    def init_hud_shader(self):
        """Return compiled HUD shader."""

        v_shader = load_vshader('shaders_data/test.vs')
        f_shader = load_fshader('shaders_data/hud.fs')

        program = compile_program(v_shader, f_shader)

        return program

    def init_line_shader(self):
        """Return compiled line shader."""

        v_shader = load_vshader('shaders_data/test.vs')
        f_shader = load_fshader('shaders_data/black.fs')

        program = compile_program(v_shader, f_shader)

        return program
