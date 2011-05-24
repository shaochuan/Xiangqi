try:
    import Image
except ImportError:
    import PIL.Image as Image
from OpenGL.GL import *

class TextureLoader(object):
    def __init__(self):
        self.cache = {}

    def load(self, fname):
        if self.cache.get(fname):
            return self.cache[fname]

        texture = self.cache[fname] = glGenTextures(1)
        image = Image.open(fname)

        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBA", 0, -1)

        # Create Texture
        glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
        #glEnable(GL_TEXTURE_2D)

        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, ix, iy, 1, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

        return texture

texture = TextureLoader()
