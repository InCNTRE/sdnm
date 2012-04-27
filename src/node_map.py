import wx
import math
import topo
import os

class NodeMap(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        # Art
        node = wx.Image('img/node.png', wx.BITMAP_TYPE_PNG)
        node_h = wx.Image('img/node_h.png', wx.BITMAP_TYPE_PNG)
        node_s = wx.Image('img/node_s.png', wx.BITMAP_TYPE_PNG)
        node_sh = wx.Image('img/node_sh.png', wx.BITMAP_TYPE_PNG)
        node_d = wx.Image('img/node_d.png', wx.BITMAP_TYPE_PNG)
        node_dh = wx.Image('img/node_dh.png', wx.BITMAP_TYPE_PNG)
        self.node = node.ConvertToBitmap()
        self.node_h = node_h.ConvertToBitmap()
        self.node_s = node_s.ConvertToBitmap()
        self.node_sh = node_sh.ConvertToBitmap()
        self.node_d = node_d.ConvertToBitmap()
        self.node_dh = node_dh.ConvertToBitmap()

        # Initialize params
        self.save_fd = None
        self.show_macs = False
        self.show_ports = False
        self.counter = 0
        self.selected = ""

        # Initialize node_map state
        self.state = topo.Topology()
        
        # Bind to events
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

    def SetOpt(self, option):
        if option == 'show_macs':
            self.show_macs = not self.show_macs
        elif option == 'show_ports':
            self.show_ports = not self.show_ports
        else:
            pass

    def Capture(self, fd):
        self.save_fd = fd

    def find_node_pos(self, mac):
        for node in self.nodes:
            if node.mac == mac:
                return node.GetPos()
        return False

    def OnPaint(self, event):
        """
        Redraw image to screen and save if self.save_fd != None
        """
        dc = wx.PaintDC(self)
        dc.Clear()

        for link in self.state.GetLinks():
            # Update Drawing code
            src_pos = link.srcpos
            dst_pos = link.dstpos
            dc.SetPen(wx.Pen(wx.Colour(255,255,255)))
            dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))

            if link.info or self.show_ports:
                s = 'src_port: ' + str(link.srcport) + '\ndst_port: ' + str(link.dstport)
                x = (src_pos[0]+dst_pos[0])/2 - 20
                y = (src_pos[1]+dst_pos[1])/2 - 10
                
                tw, th = dc.GetTextExtent(s)
                dc.DrawRectangle(x, y, tw, th)
                dc.DrawText(s, x, y)
            
            if link.dead:
                dc.SetPen(wx.Pen(wx.Colour(255,0,0), 2))
            else:
                dc.SetPen(wx.Pen(wx.Colour(58,58,58), 2))
            dc.DrawLine(src_pos[0], src_pos[1],
                        dst_pos[0], dst_pos[1])

        for node in self.state.GetNodes():
            x, y = (node.x,node.y)
            w, h = (node.w,node.h)

            if node.info or self.show_macs:
                dc.SetPen(wx.Pen(wx.Colour(58,58,58)))
                dc.DrawText(node.mac, x-60, y+20)
            #if not node.hover and not node.select:
            #    dc.DrawBitmap(self.node, x-w/2, y-h/2)
            #elif node.hover and node.select:
            #    dc.DrawBitmap(self.node_sh, x-w/2, y-h/2)
            #elif node.hover:
            #    dc.DrawBitmap(self.node_h, x-w/2, y-h/2)
            #else:
            #    dc.DrawBitmap(self.node_s, x-w/2, y-h/2)

            if node.hover:
                if node.select:
                    dc.DrawBitmap(self.node_sh, x-w/2, y-h/2)
                elif node.dead:
                    dc.DrawBitmap(self.node_dh, x-w/2, y-h/2)
                else:
                    dc.DrawBitmap(self.node_h, x-w/2, y-h/2)
            else:
                if node.select:
                    dc.DrawBitmap(self.node_s, x-w/2, y-h/2)
                elif node.dead:
                    dc.DrawBitmap(self.node_d, x-w/2, y-h/2)
                else:
                    dc.DrawBitmap(self.node, x-w/2, y-h/2)

        if self.save_fd != None:
            size = self.GetSize()
            
            bmp = wx.EmptyBitmap(size[0], size[1])
            memDC = wx.MemoryDC()
            
            memDC.SelectObject(bmp)
            memDC.Blit(0, 0, size[0], size[1], dc, 0, 0)
            memDC.SelectObject(wx.NullBitmap)

            img = bmp.ConvertToImage()
            img.SaveFile(self.save_fd, wx.BITMAP_TYPE_PNG)
            self.save_fd = None

    def Update(self):
        """
        Update network_graph data
        """
        self.counter += 1
        if self.counter > 150:
            self.state.Update()
            self.counter = 0

        self.Refresh()

    def OnMouse(self, event):
        mX = event.GetX()
        mY = event.GetY()

        for node in self.state.GetNodes():
            if node.Intersects((mX,mY)):
                node.hover = True
                node.info = True
                if event.LeftIsDown() and (self.selected=="" or self.selected==node.mac):
                    self.state.SelectNode(node.mac)
                    self.selected=node.mac
                    node.Move((mX,mY))
                    for link in self.state.GetLinks():
                        link.Move((mX,mY), node.mac)
                elif event.LeftUp():
                    self.selected = ""
                elif event.RightIsDown():
                    print 'Right is down on', node.mac
            else:
                node.hover = False
                node.info = False
        for link in self.state.GetLinks():
            if link.Intersects((mX,mY)):
                link.hover = True
            else:
                link.hover = False
