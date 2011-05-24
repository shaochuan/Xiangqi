from math import sin, cos, pi
from OpenGL.GL import *

class DrawDelegate(object):
    def onDraw(self):
        raise NotImplementedError

resolution = 64
circle_points = [(cos(t*2*pi/resolution), sin(t*2*pi/resolution)) for t in xrange(0, resolution)]

def draw_solid_ball(x,y,r=0.02,color=(0,1,0)):
    print 'solid ball'
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(*color)
    glVertex3f(x,y,0)
    for px,py in circle_points:
        glVertex3f(r*px+x, r*py+y, 0.0)
    firstx = circle_points[0][0]
    firsty = circle_points[0][1]
    glVertex3f(r*firstx + x, r*firsty+y,0.0)
    glEnd()

