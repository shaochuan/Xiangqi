from OpenGL.GLUT import glutPostRedisplay

class MouseDelegate(object):
  def onMouse(self, *args):
    raise NotImplementedError


class KeyDelegate(object):
  def onKey(self, *args):
    raise NotImplementedError

g_events = []
def null_action():
  return False

class Event(object):
  def __init__(self, _type, msg='', action=null_action):
    self.action = action  # callable, will return True if redraw needed.
    self._type = _type
    self.msg = msg

def post_event(event):
  g_events.append(event)

def consume_events(app):
  for e in g_events[:]:
    app.handle_event(e)
    g_events.pop(0)

