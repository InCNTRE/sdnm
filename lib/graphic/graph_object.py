import sys
import wx

sys.path.append("./lib")
import gmath

def DrawLink(dc, link):
    """ Draw @link to the screen
    """
    srcpos = link.srcpos
    dstpos = link.dstpos

    if link.dead:
        dc.SetPen(wx.Pen(wx.Colour(255,0,0), 2))
    else:
        dc.SetPen(wx.Pen(wx.Colour(58,58,58), 2))
    dc.DrawLine(srcpos[0], srcpos[1],
                dstpos[0], dstpos[1])

    # If extra info is desired draw ports
    if link.hover or link.info:
        dc.SetPen(wx.Pen(wx.Colour(58,58,58), 1))
        dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))

        # Draw srcport
        sx, sy = gmath.PointOnLine(dstpos, srcpos, -30)
        ss = str(link.srcport)
        sw, sh = dc.GetTextExtent(ss)
        dc.DrawRectangle(sx-3, sy-3, sw+6, sh+6)
        # Draw dstport
        dx, dy = gmath.PointOnLine(srcpos, dstpos, -30)
        ds = str(link.dstport)
        dw, dh = dc.GetTextExtent(ds)
        dc.DrawRectangle(dx-3, dy-3, dw+6, dh+6)

        dc.DrawText(ss, sx, sy)
        dc.DrawText(ds, dx, dy)
