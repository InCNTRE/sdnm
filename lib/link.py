"""
link.py defines a Node structure
"""
import math

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
        #print rect[0], mX, rect[2], '\t', rect[1], mY, rect[3]
        if (mX > rect[0] and mX < rect[2] and
            mY > rect[1] and mY < rect[3]):
            self.info = True
        else:
            self.info = False

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
        xdif = self._x2 - self._x1
        ydif = self._y2 - self._y1
        _len = math.sqrt( math.pow(xdif, 2) +
                         math.pow(ydif, 2))
        cntr = ((self._x2 + self._x1) / 2, (self._y2 + self._y1) / 2)

        a = math.atan(ydif/xdif)
        #print('Slope: ' + str(ydif) + '/' + str(xdif) + '\n' + 'Degrees: ' + str(math.degrees(a)))

        # This gives us a bounding box, unrotated with
        # a center at the center of the link.
        r = []
        r.append((cntr[0]-_len/2, cntr[1]-1))
        r.append((cntr[0]+_len/2, cntr[1]+1))

        r1 = []
        for p in r:
            s = math.sin(a)
            c = math.cos(a)

            p0 = p[0] - cntr[0]
            p1 = p[1] - cntr[1]

            x = (p0 * c - p1 * s)
            y = (p0 * s + p1 * c)

            p0 = x + cntr[0]
            p1 = y + cntr[1]
            r1.append((p0,p1))

        if math.degrees(a) >= 0:
            return (r1[0][0],r1[0][1],r1[1][0],r1[1][1])
        else:
            return (r1[0][0],r1[1][1],r1[1][0],r1[0][1])

    def Update(self, pos):
        if self.Intersects(pos):
            self.info = True
            self.hover = True
        else:
            self.hover = False
