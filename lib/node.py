"""
node.py defines a Node structure
"""
class Node(object):
    def __init__(self, x=0, y=0, w=0, h=0, mac='00:00:00:00:00:00'):
        self._x = 0
        self._y = 0
        self._w = 0
        self._h = 0
        self._mac = ''

        self._info = False
        self._hover = False
        self._select = False

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, v):
        self._x = v

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, v):
        self._y = v

    @property
    def w(self):
        return self._w
    @w.setter
    def w(self, v):
        self._w = v

    @property
    def h(self):
        return self._h
    @h.setter
    def h(self, v):
        self._h = v

    @property
    def mac(self):
        return self._mac
    @mac.setter
    def mac(self, v):
        self._mac = v

    @property
    def info(self):
        return self._info
    @info.setter
    def info(self, v):
        self._info = v

    @property
    def hover(self):
        return self._hover
    @hover.setter
    def hover(self, v):
        self._hover = v

    @property
    def select(self):
        return self._select
    @select.setter
    def select(self, v):
        self._select = v

    # END: Getters, Setters
    # BEGIN: Class functions
    
    def Intersects(self, pos):
        mX, mY = pos
        w2 = self.w/2
        h2 = self.h/2
        print(mX, mY)
        if (mX > self.x-w2 and mX < self.x+w2 and
            mY > self.y-h2 and mY < self.y+h2):
            return True
        else:
            return False
    
    def Move(self, pos):
        self.x, self.y = pos
        self.select = True

    def Update(self, pos):
        if self.Intersects(pos):
            self.info = True
            self.hover = True
            return True
        else:
            self.hover = False
            return False
