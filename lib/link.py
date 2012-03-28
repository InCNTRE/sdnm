"""
link.py defines a Node structure
"""
class Link(object):
    def __init__(self, srcmac='', srcport=0, dstmac='', dstport=0):
        self._x1 = 0
        self._y1 = 0
        self._x2 = 0
        self._y2 = 0
        self._srcmac = srcmac
        self._srcport = srcport
        self._dstmac = dstmac
        self._dstport = dstport

        self._info = False
        self._hover = False
        self._select = False

    @property
    def srcmac(self):
        return self._srcmac
    @srcmac.setter
    def srcmac(self, v):
        self._srcmac = v

    @property
    def srcpos(self):
        return (self._x1, self._y1)

    @property
    def srcport(self):
        return self._srcport
    @srcport.setter
    def srcport(self, v):
        self._srcport = v

    @property
    def dstmac(self):
        return self._dstmac
    @dstmac.setter
    def dstmac(self, v):
        self._dstmac = v

    @property
    def dstpos(self):
        return (self._x2, self._y2)

    @property
    def dstport(self):
        return self._dstport
    @dstport.setter
    def dstport(self, v):
        self._dstport = v

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
        rect = self.Rectangle()
        if (mX > rect[0] and mX < rect[2] and
            mY > rect[1] and mY < rect[3]):
            return True
        else:
            return False

    def LinkAsDict(self):
        return {'src-switch': self.srcmac, 'dst-switch': self.dstmac,
                'src-port': self.srcport, 'dst-port': self.dstport}
    
    def Move(self, pos, mac):
        if mac == self.srcmac:
            self._x1, self._y1 = pos
        elif mac == self.dstmac:
            self._x2, self._y2 = pos
        else:
            pass
            #print('invalid position id')

    def Rectangle(self):
        r0 = 0
        r1 = 0
        r2 = 0
        r3 = 0
        if self._x1 < self._x2:
            r0 = self._x1-1
            r2 = self._x2+1
        elif self._x1 > self._x2:
            r0 = self._x1+1
            r2 = self._x2-1
        else:
            r0 = self._x1
            r2 = self._x2
        if self._y1 < self._y2:
            r1 = self._y1-1
            r3 = self._y2+1
        elif self._y1 > self._y2:
            r1 = self._y1+1
            r3 = self._y2-1
        else:
            r1 = self._y1
            r3 = self._y2
        return (r0,r1,r2,r3)

    def Update(self, pos):
        if self.Intersects(pos):
            self.info = True
            self.hover = True
        else:
            self.hover = False
