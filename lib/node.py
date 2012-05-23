"""
node.py defines a Node structure
"""
class Node(object):
    def __init__(self, x=0, y=0, w=0, h=0, mac='00:00:00:00:00:00'):
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._mac = mac
        self._desc = None

        self._info = False
        self._hover = False
        self._select = False
        self._dead = False

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
    def desc(self):
        return self._desc
    @desc.setter
    def desc(self, v):
        self._desc = v

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

    @property
    def dead(self):
        return self._dead
    @dead.setter
    def dead(self, v):
        self._dead = v

    def GetPos(self):
        return (self.x, self.y)

    def DistanceToPoint(self, point):
        """Return distance to point from self
        Args:
        point: (x,y) cords to calculate distance to
        """
        a = self.x - point[0]
        b = self.y - point[1]
        c = math.sqrt(a*a + b*b)
        return c

    def Intersects(self, pos):
        mX, mY = pos
        w = self.w/2
        h = self.h/2
        if (mX > self.x-w and mX < self.x+w and
            mY > self.y-h and mY < self.y+h):
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
