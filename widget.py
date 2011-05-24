from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import draw
import event
import resource
from os.path import join

def circulaate(length):
    if length <= 2:
        return
    for x in xrange(length-1):
        yield (x, x+1)
    yield (length-1, 0)


class Piece(object):
    LABELS = ['GENERAL',
        'ADVISOR',
        'ELEPHANT',
        'HORSE',
        'CHARIOT',
        'CANNON',
        'SOLDIER']

    namemap = {}
    for _id, label in enumerate(LABELS):
        namemap[_id] = label
        locals()[label] = _id

    UISTATE = ['NONE', 'PRESSED', 'SELECTED']
    statemap = {}
    for _id, state in enumerate(UISTATE):
        statemap[_id] = state
        locals()[state] = _id


    def __init__(self, _type, color='red'):
        self._type = _type
        self.color = color
        self.state = self.NONE
        self.texture = resource.texture.load(self.imgpath)

    def __repr__(self):
        return '%s: %s, %s' % (self.color, self.label, self.state)

    @property
    def label(self):
        return self.namemap[self._type]

    @property
    def imgpath(self):
        return join('images', join(self.color, self.label.capitalize() +
                '.png'))

    @property
    def is_selected(self):
        return self.state == self.SELECTED

    def draw(self, vx, vy):
        glPushMatrix()
        glTranslatef(vx, vy, 0.0)
        quadratic = gluNewQuadric()
        gluQuadricNormals(quadratic, GLU_SMOOTH)		# Create Smooth Normals (NEW)
        gluQuadricTexture(quadratic, GL_TRUE)			# Create Texture Coords (NEW)
        if self.is_selected:
            glColor3f(0,1,0)
            gluDisk(quadratic,0.0,0.11,16, 64)
        else:
            glColor4f(0,0,0,1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glEnable(GL_TEXTURE_2D)
        gluDisk(quadratic,0.0,0.1,16, 64)
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()


class Board(draw.DrawDelegate, event.MouseDelegate):
    gx = 8  # grid number in x-axis
    gy = 9  # grid number in y-axis
    def __init__(self, size):
        self.size = size
        self.pieces = {}    # { logical tuple : Piece obj } expect each obj has draw method
        self.color = (1.0,0.0,0.0)
        self.border = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        self.dx = 2.0/float(self.gx)
        self.dy = 2.0/float(self.gy)
        self.z = -3.0
        self.modelview = None
        self.projectview = None
        self.viewport = None
        self.screenz = None

    def onInit(self):
        initpieces = {
                (4,9) : Piece.GENERAL,
                (3,9) : Piece.ADVISOR,
                (5,9) : Piece.ADVISOR,
                (2,9) : Piece.ELEPHANT,
                (6,9) : Piece.ELEPHANT,
                (1,9) : Piece.HORSE,
                (7,9) : Piece.HORSE,
                (0,9) : Piece.CHARIOT,
                (8,9) : Piece.CHARIOT,
                (6,7) : Piece.CANNON,
                (2,7) : Piece.CANNON,
                (0,6) : Piece.SOLDIER,
                (2,6) : Piece.SOLDIER,
                (4,6) : Piece.SOLDIER,
                (6,6) : Piece.SOLDIER,
                (8,6) : Piece.SOLDIER,
                }
        for c, _type in initpieces.iteritems():
            self.pieces[c] = Piece(_type, 'red')
            ix, iy=c
            d = (ix, -iy+self.gy)
            self.pieces[d] = Piece(_type, 'black')

    @property
    def width(self):
        return float(self.size[0])
    @property
    def height(self):
        return float(self.size[1])

    def onMouse(self, button, state, x, y):
        if self.modelview is None or \
                self.projectview is None or \
                self.viewport is None or \
                self.screenz is None:
            return
        if button==GLUT_LEFT_BUTTON:
            wx, wy, wz = gluUnProject(x, y, self.screenz, 
                            self.modelview,
                            self.projectview,
                            self.viewport)

            # convert to logical coordinate
            print wx, wy
            lc = self.view2logical(wx,wy)
            print lc
            piece = self.pieces.get(lc)
            if state == GLUT_DOWN:
                for p in self.pieces.values(): p.state = Piece.NONE
                piece.state = Piece.PRESSED
            if piece.state == Piece.PRESSED and state == GLUT_UP:
                piece.state = Piece.SELECTED

            print piece


    def logical2view(self, x, y):
        return (-1+self.dx*x, 1-self.dy*y)

    def view2logical(self, x, y):
        for ix in xrange(0,self.gx+1):
            fx = float(ix) - 0.5
            if -1 + self.dx * fx < x < -1 + self.dx * (fx+1):
                break
        for iy in xrange(0,self.gy+1):
            fy = float(iy) - 0.5
            if -1 + self.dy * fy < y < -1 + self.dy * (fy+1):
                break
        return ix, iy

    def drawBorder(self):
        # draw the border
        for i,j in circulaate(len(self.border)):
            px,py = self.border[i]
            qx,qy = self.border[j]
            glVertex3f(px, py, 0)
            glVertex3f(qx, qy, 0)

    def drawHorizons(self):
        r = self.dy
        for y in xrange(1,self.gy):
            glVertex3f(-1, -1+r*y, 0)
            glVertex3f(1, -1+r*y, 0)

    def drawVerticals(self):
        rx = self.dx
        ry = self.dy
        for x in xrange(1,self.gx):
            glVertex3f(-1+rx*x, -1+ry*5, 0)
            glVertex3f(-1+rx*x, 1, 0)
        for x in xrange(1,self.gx):
            glVertex3f(-1+rx*x, -1+ry*4, 0)
            glVertex3f(-1+rx*x, -1, 0)

    def onDraw(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, self.z)

        glPushMatrix()
        glLineWidth(2)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        glScale(1, self.height/self.width, 1)

        self.modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        self.projectview = glGetDoublev(GL_PROJECTION_MATRIX)
        self.viewport = glGetIntegerv(GL_VIEWPORT)
        _,__,self.screenz = gluProject(0,1,0,self.modelview,
                         self.projectview,
                         self.viewport)
        # draw the grid
        glBegin(GL_LINES)
        glColor3f(*self.color)
        self.drawBorder()
        self.drawHorizons()
        self.drawVerticals()
        glEnd()

        # draw the outer border
        glPushMatrix()
        glScale(1.02, 1.015, 1.02)
        glBegin(GL_LINES)
        self.drawBorder()
        glEnd()
        glPopMatrix()

        # draw the pieces
        for ic, p in self.pieces.iteritems():
            p.draw(*self.logical2view(*ic))

        glPopMatrix()


        glutSwapBuffers()

