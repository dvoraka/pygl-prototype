# -*- coding: utf-8 -*-
#

from OpenGL.GL.shaders import *


def read_shader(filename):
    '''Read shader program from file and return it as a string.'''
    
    with open(filename) as fh:
        
        shader = ''
        for line in fh:

            shader += line

    return shader


def load_vshader(filename):
    '''Return compiled vertex shader.'''
    
    shader = read_shader(filename)
    vshader = compileShader(shader, GL_VERTEX_SHADER)

    return vshader


def load_fshader(filename):
    '''Return compiled fragment shader.'''
    
    shader = read_shader(filename)
    fshader = compileShader(shader, GL_FRAGMENT_SHADER)

    return fshader


def compileProg(*shaders):
    '''Compile shader program.'''

    return compileProgram(*shaders)
