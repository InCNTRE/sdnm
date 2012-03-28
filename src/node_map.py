import wx
import math
import topo

class NodeMap(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        # Art
        node = wx.Image('../img/node.png', wx.BITMAP_TYPE_PNG)
        node_h = wx.Image('../img/node_h.png', wx.BITMAP_TYPE_PNG)
        node_s = wx.Image('../img/node_s.png', wx.BITMAP_TYPE_PNG)
        self.node = node.ConvertToBitmap()
        self.node_h = node_h.ConvertToBitmap()
        self.node_s = node_s.ConvertToBitmap()

        # Initialize params
        self.save_fd = None
        self.show_macs = False
        self.show_ports = False
        self.counter = 0
        self.selected = ""

        # Initialize node_map state
        self.state = topo.Topology()

        #for mac, pos in self.topo.get_nodes().iteritems():
        #    self.add_node(pos[0], pos[1], mac)
        #for link in self.topo.get_links():
        #    self.add_link(link['src-port'], link['dst-port'], link['src-switch'], link['dst-switch'])
        
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

    def add_node(self, x, y, mac):
        self.nodes.append(Node(x, y, mac))

    def find_node_pos(self, mac):
        for node in self.nodes:
            if node.GetMac() == mac:
                return node.GetPos()
        return False

    def add_link(self, src_port, dst_port, src_mac, dst_mac):
        src_pos = self.find_node_pos(src_mac)
        dst_pos = self.find_node_pos(dst_mac)
        self.links.append(Link(src_pos, dst_pos, src_port, dst_port, src_mac, dst_mac))

    def OnPaint(self, event):
        """
        Redraw image to screen and save if self.save_fd != None
        """
        dc = wx.PaintDC(self)
        dc.Clear()

        for link in self.state.GetLinks():
            # Update Drawing code
            src_pos = link.GetSrcPos()
            dst_pos = link.GetDstPos()
            dc.SetPen(wx.Pen(wx.Colour(58,58,58), 2))
            
            if link.Viewable() or self.show_ports:
                s = 'src_port: ' + str(link.GetSrcPort()) + '\ndst_port: ' + str(link.GetDstPort())
                x = (src_pos[0]+dst_pos[0])/2 - 20
                y = (src_pos[1]+dst_pos[1])/2 - 10
                dc.DrawText(s, x, y)
            dc.DrawLine(src_pos[0], src_pos[1],
                        dst_pos[0], dst_pos[1])

        for node in self.state.GetNodes():
            x, y = node.GetPos()
            w, h = node.GetDim()

            if node.Viewable() or self.show_macs:
                dc.SetPen(wx.Pen(wx.Colour(58,58,58)))
                dc.DrawText(node.GetMac(), x-60, y+20)
            state = node.GetState()
            if state == 'node':
                dc.DrawBitmap(self.node, x-w/2, y-h/2)
            elif state == 'node_h':
                dc.DrawBitmap(self.node_h, x-w/2, y-h/2)
            else:
                dc.DrawBitmap(self.node_s, x-w/2, y-h/2)

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

        if event.Moving():
            for node in self.state.GetNodes():
                if node.Update(mX, mY):
                    for l in self.state.GetLinks():
                        l.Update(node.GetMac(), node.GetPos(), mX, mY)
        elif event.LeftIsDown():
            for node in self.state.GetNodes():
                if node.Intersects(mX, mY) and (self.selected=="" or self.selected==node.GetMac()):
                    self.selected = node.GetMac()
                    self.state.SelectNode(node.GetMac())
                    node.Move(mX, mY)
                    for l in self.state.GetLinks():
                        l.Update(node.GetMac(), node.GetPos(), mX, mY)
        elif event.LeftUp():
            self.selected = ""
