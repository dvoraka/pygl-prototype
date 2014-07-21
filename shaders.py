# -*- coding: utf-8 -*-
#

"""Module for shaders."""


from OpenGL.GL import GL_VERTEX_SHADER
from OpenGL.GL import GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileShader
from OpenGL.GL.shaders import compileProgram


def read_shader(filename):
    """Read shader program from file and return it as a string."""

    with open(filename) as fh:

        shader = ''
        for line in fh:

            shader += line

    return shader


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
