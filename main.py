import wx
import os
import sys
sys.path.append("/")
from src import node_map


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        # Arrange layout
        self.node_map = node_map.NodeMap(self, -1)
        self.node_map.SetBackgroundColour(wx.Colour(58,58,58))

        #self.port_list = wx.Panel(self)
        #self.port_list.SetBackgroundColour(wx.Colour(255,0,0))

        #self.port_graph = wx.Panel(self)
        #self.port_graph.SetBackgroundColour(wx.Colour(0,255,0))

        #self.port_counter = wx.Panel(self)
        #self.port_counter.SetBackgroundColour(wx.Colour(0,0,255))

        hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.node_map, 3, wx.EXPAND | wx.ALL, 3)
        #hBox1.Add(self.port_list, 1, wx.EXPAND | wx.ALL, 3)

        hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        #hBox2.Add(self.port_graph, 3, wx.EXPAND | wx.ALL, 3)
        #hBox2.Add(self.port_counter, 1, wx.EXPAND | wx.ALL, 3)

        vBox1 = wx.BoxSizer(wx.VERTICAL)
        vBox1.Add(hBox1, 3, wx.EXPAND, 3)
        #vBox1.Add(hBox2, 1, wx.EXPAND, 3)

        self.SetSizer(vBox1)

        # Setup menubar
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, 'E&xit', 'Close this program')
        menubar.Append(file_menu, '&File')

        view_menu = wx.Menu()
        view_menu.Append(201, '&Mac Address', 'View mac addresses')
        view_menu.Append(202, 'Link &Ports', 'View src and dst link ports')
        menubar.Append(view_menu, '&View')

        capture_menu = wx.Menu()
        capture_menu.Append(301, '&Network graph', 'Capture network graph')
        menubar.Append(capture_menu, '&Capture')

        help_menu = wx.Menu()
        help_menu.Append(401, 'Known &Issues', 'List known bugs and issues')
        help_menu.Append(402, '&About', 'About this program')
        menubar.Append(help_menu, '&Help')

        self.SetMenuBar(menubar)
        self.CreateStatusBar()

        # Bind to events
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.ViewMac, id=201)
        self.Bind(wx.EVT_MENU, self.ViewLinkPort, id=202)
        self.Bind(wx.EVT_MENU, self.CaptureNetworkGraph, id=301)
        self.Bind(wx.EVT_MENU, self.KnownIssues, id=401)
        self.Bind(wx.EVT_MENU, self.Help, id=402)

        self.Bind(wx.EVT_TIMER, self.OnTimer)

        # Setup update Timer
        self.timer = wx.Timer(self)
        self.timer.Start(20)

    # Events
    def OnClose(self, event):
        self.Destroy()

    def ViewMac(self, event):
        self.node_map.SetOpt('show_macs')

    def ViewLinkPort(self, event):
        self.node_map.SetOpt('show_ports')

    def CaptureNetworkGraph(self, event):
        dlg = wx.FileDialog(self, "Save image", os.getcwd(), "", "*.png", wx.SAVE)
        dlg.SetFilename('graph.png')

        if dlg.ShowModal() == wx.ID_OK:
            self.node_map.Capture(dlg.GetPath())
        dlg.Destroy()

    def KnownIssues(self, event):
        pass

    def Help(self, event):
        pass

    def OnTimer(self, event):
        self.node_map.Update()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Title.py')
        frame.Show()
        return True

app = MyApp(0)
app.MainLoop()
