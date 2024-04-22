import numpy as np

from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image

materials: dict[str, int] = {}


def load_texture(filename):
    img = Image.open(filename)
    img_data = img.tobytes("raw", "RGBX", 0, -1)
    width, height = img.size
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    return texture_id


def get(filename):
    if filename in materials:
        return materials[filename]
    else:
        material_id = load_texture(filename)
        materials[filename] = material_id
        return material_id
