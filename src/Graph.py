import sys, os
import MySQLdb as mdb
import json
import logging

DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = 'fucksec'
DB     = 'stacktrack'

OUTDIR = '/var/u/json'

con = mdb.connect(DBHOST,DBUSER,DBPASS,DB)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class Graph():

    def __init__(self):

        self.nodes  = {}
    
    def add_node(self,node):
        '''
           Can be instantiated from 
           - string (node name)
           - Node type 
           - (json) dict

           There can only be one node with the same name. If the name 
           already exists in _instances, the corresponding node value
           is returned
        '''

        callees     = set()
        callers     = set()
        sourcefile  = ''

        if type(node) == Node:
            name = node.name

        elif type(node) in (str,):
            name = node

        else: #todo: error checking ... 
            log.critical('Unknown type "{}"'.format(type(node)))

        if name not in self.nodes:

            log.debug('Creating Node {} {}'.format(name,len(self.nodes)))
            node =  Node(name, sourcefile, callees, callers )
            self.nodes[name] =  node

        node = self.nodes[name]
        return node

    def get_node(self,node_name):
        
        return self.nodes.get(node_name,None)


    def get_nodes(self):

        return self.nodes.values()

    def add_edge(self, caller, callee):
        '''
            This creates a link between two nodes
            if the nodes don't exist they are created
        '''
        caller_node = self.add_node(caller)
        callee_node = self.add_node(callee)
        caller_node.add_callee(callee_node)
        callee_node.add_caller(caller_node)
        return caller_node, callee_node

    def load(self, load_callers = True, load_callees = True):
        '''
            Load all nodes. This will run until all nodes
            are processed
        '''
        loaded = set()

        nodes = set(self.get_nodes())
        while loaded != nodes : #set(self.get_nodes()):
            for node in nodes:
                if not node in loaded:
                    self.load_node(node, load_callers, load_callees)
                    loaded.add(node)

            nodes = set(self.get_nodes())


    def load_node(self, node , load_callers = True, load_callees = True):
        '''
            Get the xrefs from the database and create an edge
            (edge creation causes not-yet-existing nodes to be created)
        '''
        
        log.debug('Loading {}'.format(node))

        cursor  = con.cursor(mdb.cursors.DictCursor)

        query = ''' SELECT caller, callee
                    FROM xrefs
                    WHERE 
                        caller COLLATE latin1_general_cs LIKE %s 
                        OR 
                        callee COLLATE latin1_general_cs LIKE %s
                '''

        if load_callers and load_callees:
            cursor.execute(query,(node.name,node.name))
        elif load_callers:
            cursor.execute(query,(None,node.name))
        elif load_callees:
            cursor.execute(query,(node.name,None))
        else:
            return
        rows = cursor.fetchall()
        for row in rows:
            callee_name     = row['callee']
            caller_name     = row['caller']
            #if callee_name == caller_name:
            caller, callee  = self.add_edge(caller_name,callee_name)

    def dump_nodes(self, destdir = '.'):
        for node in self.get_nodes():
            self.dump_node(node,destdir)
    
    def dump_node(self,node,destdir):
        outfile = os.path.join(destdir,node.name + '.json' )
        log.debug('dumping {} to {}'.format(node,outfile))
        if node.get_callers() or not node.get_callees():
            log.debug('Ignoring {}'.format(node))
            return
        with open(outfile, 'w+') as f:
            f.write(json.dumps(node,cls=NodeEncoder,indent=True,check_circular=False))



class Node(object):

    def __init__(self, name, sourcefile, callees, callers ):

        self.name       = name
        self.loaded     = False
        self.callers    = callers
        self.callees    = callees
        self.sourcefile = sourcefile

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'Node {0}'.format(self.name)

    def __str__(self):
        return self.__repr__()

    def add_caller(self,node):
        self.callers.add(node)

    def add_callee(self,node):
        self.callees.add(node)

    def get_callers(self):
        return self.callers

    def get_callees(self):
        return self.callees
           

class NodeEncoder(json.JSONEncoder):
    '''
        Encodes nodes, the processed variable is used 
        to avoid circular references
    '''
    '''def __new__(cls,*args,**kwargs):

        instance = super(NodeEncoder,cls).__new__(cls,*args,**kwargs)
        instance.processed = set()
        return instance
    '''
    def __init__(self, *args, **kwargs):
        super(NodeEncoder, self).__init__(*args, **kwargs)
        self.processed = set()

    def default(self,object):

        if isinstance(object,Node):
            return self.encode_node(object)


    def encode_node(self,node):
        '''
            encode a node as a d3 json object
        '''
            
        log.debug('Encoding {}'.format(node.name))
        if node in self.processed :
            
            log.debug("Already Processed {}".format(node.name))
            result ={ "name"     : node.name,
                      "label"    : node.name,
                      "type"     : "duplicate",
                   }

        else:
            self.processed.add(node)
            children = []
            for child in getattr(node,'callees'):
                children.append(child)

            result = {  "name"      : node.name, 
                        "label"     : node.name,
                        "size"      : 1 ,
                        "sourcefile": node.sourcefile,
                        "type"      : "original",
                        "children"  : children
                     }

        return result


def main():
    nodenames = sys.argv[1:]
    g = Graph()
    for noden in nodenames:
        node = g.add_node(noden)
    g.load(load_callers = False, load_callees = True)
    g.dump_nodes(OUTDIR)
    exit()


if __name__ == '__main__':
    main()
