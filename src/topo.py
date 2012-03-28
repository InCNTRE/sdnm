import ast
import math
import subprocess
import networkx as nx
from networkx import graphviz_layout
import matplotlib.pylab as plt

from .lib.link import Link
from .lib.node import Node

"""
class Link(object):
    def __init__(self, src_pos, dst_pos, src_port, dst_port, src, dst):
        self.src_pos = src_pos
        self.dst_pos = dst_pos
        #self.color = wx.Colour(58,58,58)
        # Network
        self.src_port = src_port
        self.dst_port = dst_port
        self.src = src
        self.dst = dst
        # Interative Params
        self.view_ports = False

    def LinkAsDict(self):
        return {'src-switch': self.src, 'dst-switch': self.dst,
                'src-port': self.src_port, 'dst-port': self.dst_port}

    def SetSrcPos(self, pos):
        self.src_pos = pos

    def SetDstPos(self, pos):
        self.dst_pos = pos
    
    def GetSrcPos(self):
        return self.src_pos

    def GetDstPos(self):
        return self.dst_pos

    def GetSrcMac(self):
        return self.src

    def GetSrcPort(self):
        return self.src_port
    def GetDstPort(self):
        return self.dst_port

    def GetDstMac(self):
        return self.dst

    def Viewable(self):
        return self.view_ports

    def Update(self, mac, pos, mX, mY):
        if mac == self.src:
            self.src_pos = (pos[0], pos[1])
        elif mac == self.dst:
            self.dst_pos = (pos[0], pos[1])
        else:
            pass

    def Move(self, src_pos, dst_pos):
        self.src_pos = src_pos
        self.dst_pos = dst_pos

class Node(object):
    def __init__(self, x, y, mac):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 40

        # Interative Params
        self.view_mac = False
        self.selected = False
        self.state = 'node'

        # Network
        self.mac = mac

    def Select(self):
        self.selected = True
        return self.mac

    def Deselect(self):
        self.selected = False

    def Viewable(self):
        return self.view_mac

    def GetPos(self):
        return (self.x, self.y)

    def GetDim(self):
        return (self.w, self.h)

    def GetState(self):
        return self.state

    def SetPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def GetMac(self):
        return self.mac
    
    def Intersects(self, mouse_x, mouse_y):
        if (mouse_x > self.x-self.w/2 and mouse_x < self.x+self.w/2 and
            mouse_y > self.y-self.h/2 and mouse_y < self.y+self.h/2):
            return True
        else:
            return False

    def Move(self, mouse_x, mouse_y):
            self.x = mouse_x
            self.y = mouse_y

    def Update(self, mouse_x, mouse_y):
        if (mouse_x > self.x-self.w/2 and mouse_x < self.x+self.w/2 and
            mouse_y > self.y-self.h/2 and mouse_y < self.y+self.h/2):
            self.state = 'node_h'
            self.view_mac = True
            return True
        else:
            if self.selected:
                self.state = 'node_s'
            else:
                self.state = 'node'
                self.view_mac = False
            return False
"""

class Topology():
    def __init__(self, ip='127.0.0.1', port='8080'):
        self.nodes = []
        self.new_nodes = []
        self.links = []
        self.new_links = []
        # Params
        self.ip = ip
        self.port = port

        # Attributes
        self.selected = ''

    def SelectNode(self, mac):
        for n in self.nodes:
            if n.mac == mac:
                self.selected = mac
                n.select = True
            else:
                n.select = False         

    def GetNodes(self):
        return self.nodes
    
    def GetNode(self, mac):
        for n in self.nodes:
            if n.mac == mac:
                return n

    def GetNewNodes(self, srv_nodes):
        '''
        Returns a list of new Nodes
        '''
        result = []
        for node in srv_nodes:
            node_ex = False
            for n in self.nodes:
                if node == n.mac:
                    node_ex = True
            if not node_ex:
                result.append( Node(x=0, y=0, w=40, h=40, mac=node) )
                
        return result
    
    def RemoveDeadNodes(self, srv_nodes):
        #print(len(self.nodes))
        for i in range(len(self.nodes)):
            if self.nodes[i].mac not in srv_nodes:
                del(self.nodes[i])

    def RemoveDeadLinks(self, srv_links):
        if srv_links != None:
            for i in range(len(self.links)):
                if self.links[i].LinkAsDict() not in srv_links:
                    del(self.links[i])

    def GetOldNodes(self):
        pass
    
    def GetLinks(self):
        return self.links
    
    def RemoveDuplicateLinks(self, srv_links):
        '''
        '''
        result = []
        for link in srv_links:
            inv_link = {'src-switch': link['dst-switch'],
                        'dst-switch': link['src-switch'],
                        'src-port': link['dst-port'],
                        'dst-port': link['src-port']}
            if link not in result:
                if inv_link not in result:
                            result.append(link)
        return result
    
    def GetNewLinks(self, srv_links):
        srv_links = self.RemoveDuplicateLinks(srv_links)
        result = []
        for link in srv_links:
            link_ex = False
            for l in self.links:
                if link == l:
                    link_ex = True
            if not link_ex:
                result.append( Link(link['src-switch'], link['src-port'],
                                    link['dst-switch'], link['dst-port']) )
                
        return result

    def Update(self):
        srv_nodes = self.UpdateNodes()
        srv_links = self.UpdateLinks()

        self.new_nodes = self.GetNewNodes(srv_nodes)
        #self.RemoveDeadNodes(srv_nodes)
        self.new_links = self.GetNewLinks(srv_links)
        #self.RemoveDeadLinks(srv_links)
        self.nodes += self.new_nodes
        self.links += self.new_links

        # Get node positions for new nodes.
        node_pos = self.UpdateGraph()

        for node in self.nodes:
            if (node.x,node.y) == (0,0):
                pos = node_pos[node.mac]
                node.x = pos[0]
                node.y = pos[1]

        for link in self.links:
            s = self.GetNode(link.srcmac)
            d = self.GetNode(link.dstmac)
            link.Move((s.x, s.y), link.srcmac)
            link.Move((d.x, d.y), link.dstmac)

        #print(node_pos)
        #for node in self.new_nodes:
        #    pos = node_pos[node.GetMac()]
        #    node.SetPos(pos)
        #    self.nodes.append(node)
        self.new_nodes = []
        
        #for link in self.new_links:
        #    sp = self.GetNode(link.GetSrcMac()).GetPos()
        #    dp = self.GetNode(link.GetDstMac()).GetPos()
        #    link.SetSrcPos(sp)
        #    link.SetDstPos(dp)
        #    self.links.append(link)
        self.new_links = []

    def UpdateNodes(self):
        '''
        Retrieve node data from restAPI
        {mac: [mac1, ... , macn]}
        '''
        address = self.ip + ':' + self.port
        cq = subprocess.Popen('curl http://' + address + '/wm/topology/switchclusters/json', shell=True, stdout=subprocess.PIPE)
        cq_result = cq.communicate()[0]
        
        if cq_result == "":
            return {}
        else:
            result = []
            t = ast.literal_eval(cq_result)
            for n in t:
                for mac in t[n]:
                    result.append(mac)
            return result

    def UpdateLinks(self):
        '''
        Retrieve link data from restAPI
        {src-switch: mac, dst-switch: mac, src-port: int, dst-port: int}
        '''
        address = self.ip + ':' + self.port
        lq = subprocess.Popen('curl http://' + address + '/wm/topology/links/json', shell=True,stdout=subprocess.PIPE)
        lq_result = lq.communicate()[0]
        
        if lq_result == "":
            return []
        else:
            return ast.literal_eval(lq_result)

    def UpdateGraph(self):
        g = nx.Graph()
        for node in self.nodes:
            g.add_node(node.mac)
            for l in self.links:
                if node.mac == l.srcmac:
                    g.add_edge(l.srcmac, l.dstmac)
        # Get node positions
        return nx.graphviz_layout(g, prog='neato')
