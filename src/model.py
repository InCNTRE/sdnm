import json
import urllib

HOST = 'http://dev.damslab.org'

class UNISModel(object):
    def __init__(self, host):
        self._host = host

    def get_link(self, lid):
        fd = urllib.urlopen(self._host + '/links/' + str(lid))
        literal = fd.read()
        try:
            return json.loads(literal)
        except ValueError:
            print('[ERROR]: Malformed JSON in UNISModel.get_link')
        finally:
            fd.close()

    def get_node(self, nid):
        fd = urllib.urlopen(self._host + '/nodes/' + str(nid))
        literal = fd.read()
        try:
            return json.loads(literal)
        except ValueError:
            print('[ERROR]: Malformed JSON in UNISModel.get_node')
        finally:
            fd.close()

    def get_nodes(self):
        fd = urllib.urlopen(self._host + '/nodes')
        literal = fd.read()
        try:
            return json.loads(literal)
        except ValueError:
            print('[ERROR]: Malformed JSON in UNISModel.get_nodes')
        finally:
            fd.close()
 
    def get_links(self):
        fd = urllib.urlopen(self._host + '/links')
        literal = fd.read()
        
        try:
            return json.loads(literal)
        except ValueError:
            print('[ERROR]: Malformed JSON in UNISModel.get_links')
        finally:
            fd.close()
