
class MouseDelegate(object):
    def onMouse(self, *args):
        raise NotImplementedError


class KeyDelegate(object):
    def onKey(self, *args):
        raise NotImplementedError


