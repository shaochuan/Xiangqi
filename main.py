'''
    Xiangqi: Chinese chess game

    @date: May 23, 2011
    @author: Shao-Chuan Wang (shaochuan.wang AT gmail.com)
'''
__version__ = '1.0'

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import widget

from app import App


def getSceneFileName():
    if '-i' in sys.argv:
        ind = sys.argv.index('-i')
        return sys.argv[ind+1]
    else:
        print >> sys.stderr, "Scene File Not Found!"
        printHelp()
        sys.exit(1)

window_size = (480, 640)
window_name = 'Xiangqi'
app = App()
board = widget.Board(window_size)
app.drawDelegate = board
app.mouseDelegate = board

def initialization():
    glutInit([])
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(*window_size)
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow(window_name)
    glutDisplayFunc(app.onDraw)
    glutIdleFunc(app.onIdle)
    glutReshapeFunc(app.onResize)
    glutKeyboardFunc(app.onKey)
    glutMouseFunc(app.onMouse)

    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading

    app.onInit()

def main():
    initialization()
    glutMainLoop()

if __name__ == '__main__':
    main()
