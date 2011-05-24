from OpenGL.GL import *
from OpenGL.GLUT import glutSwapBuffers, glutPostRedisplay
from OpenGL.GLU import gluPerspective
import sys

class App(object):
    def __init__(self):
        self.drawDelegate = None   # expect has onDraw method
        self.idleDelegate = None   # expect has onIdle method
        self.keyDelegate = None    # expect callable or has onKey method
        self.mouseDelegate = None  # expect callable or has onMouse method
        self.resizeDelegate = None # expect callable or has onResize method

    def onInit(self):
        if hasattr(self.drawDelegate, 'onInit'):
            self.drawDelegate.onInit()

    def onDraw(self):
        if self.drawDelegate:
            self.drawDelegate.onDraw()
            return
        self._defaultOnDraw()

    def onIdle(self):
        if self.idleDelegate:
            self.idleDelegate.onIdle()
            return
        #glutPostRedisplay()

    def onKey(self, *args):
        if not self.keyDelegate:
            print 'key pressed:', args
            key = args[0]
            if key=='q':
                sys.exit(0)
            return

        if callable(self.keyDelegate):
            self.keyDelegate(*args)
        else:
            self.keyDelegate.onKey(*args)

    def onMouse(self, *args):
        if not self.mouseDelegate:
            return
        if callable(self.mouseDelegate):
            self.mouseDelegate(*args)
        else:
            self.mouseDelegate.onMouse(*args)

    def onResize(self, *args):
        if not self.resizeDelegate:
            self._defaultOnResize(*args)
            return
        if callable(self.resizeDelegate):
            self.resizeDelegate(*args)
        else:
            self.resizeDelegate.onResize(*args)

    def _defaultOnResize(self, width, height):
        if height == 0:
            height = 1

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(width)/float(height), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def _defaultOnDraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # We have smooth color mode on, this will blend across the vertices.
        # Draw a triangle rotated on the Y axis.
        glBegin(GL_POLYGON)                 # Start drawing a polygon
        glColor3f(1.0, 0.0, 0.0)            # Red
        glVertex3f(0.0, 1.0, 0.0)           # Top
        glColor3f(0.0, 1.0, 0.0)            # Green
        glVertex3f(1.0, -1.0, 0.0)          # Bottom Right
        glColor3f(0.0, 0.0, 1.0)            # Blue
        glVertex3f(-1.0, -1.0, 0.0)         # Bottom Left
        glEnd()

        glutSwapBuffers()

