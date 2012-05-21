"""
port.py defines a Port class
"""
class Port(object):
    def __init__(self, x=0, y=0, num=0):
        self._x = x
        self._y = y
        self._num = num

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
        return self._x
    @y.setter
    def y(self, v):
        self._y = v

    @property
    def num(self):
        return self._num
    @num.setter
    def num(self, v):
        self._num = v

    @property
    def select(self):
        return self._select
    @select.setter
    def select(self, v):
        self._select = v

    @property
    def hover(self):
        return self._hover
    @hover.setter
    def hover(self, v):
        self._hover = v

    @property
    def info(self):
        return self._info
    @info.setter
    def info(self, v):
        self._info = v

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
