#!/usr/bin/python
import sys, os
import MySQLdb as mdb
import json
import logging
import argparse


#
# Database settings
# The stacktrack database consists of an "xrefs" table 
# +--------+---------------+------+-----+---------+-------+
# | Field  | Type          | Null | Key | Default | Extra |
# +--------+---------------+------+-----+---------+-------+
# | caller | varchar(1024) | YES  |     | NULL    |       |
# | callee | varchar(1024) | YES  |     | NULL    |       |
# +--------+---------------+------+-----+---------+-------+
#
DBHOST = 'localhost'
DBUSER = 'root'
DBPASS = 'fucksec'
DB     = 'stacktrack'

class Graph():

    def __init__(self):

        self.nodes  = {}
        self.xrefdb = XRefDB()
        log.debug('Loaded xrefs')
    
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

    def get_node(self,node):
        
        node_name = node.name if type(node) == Node else node
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

        if load_callers:
            callers = self.xrefdb.get_callers(node.name)
            for caller in callers:
                self.add_edge(caller,node.name)

        if load_callees:
            callees = self.xrefdb.get_callees(node.name)
            for callee in callees:
                self.add_edge(node.name,callee)

    def dump_nodes(self, destdir = '.'):
        for node in self.get_nodes():
            self.dump_node(node,destdir)
    
    def dump_node(self, node, destdir, direction = 'callees', force = False):
        node = self.get_node(node)
        outfile = os.path.join(destdir,'{}_{}.json'.format(node.name, direction ) )
        if not getattr(node,direction):
            log.debug('{} has no {}'.format(node,direction))
            return
        inv_direction = 'callers' if direction == 'callees' else 'callees'
        if not force and getattr(node,inv_direction) :
            log.debug('{} is not a leaf for {}'.format(node,direction))
            return
        log.info('dumping {} of {} to {}'.format(direction, node, outfile))
        NodeEncoder.direction = direction
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
           

class XRefDB:

    def __init__(self):

        self.con = mdb.connect(DBHOST,DBUSER,DBPASS,DB)
        self.callee_xrefs , self.caller_xrefs = self.load_db()

    def load_db(self):
        
        query  = '''select * from xrefs'''
        cursor = self.con.cursor(mdb.cursors.DictCursor)
        cursor.execute(query)
        caller_xrefs = {}
        callee_xrefs = {}
        for row in cursor.fetchall():
            callee = row['callee']
            caller = row['caller']
            if not caller in callee_xrefs:
                callee_xrefs[caller] = set([callee])
            else:
                callee_xrefs[caller].add(callee)
            if not callee in caller_xrefs:
                caller_xrefs[callee] = set([caller])
            else:
                caller_xrefs[callee].add(caller)

        return callee_xrefs, caller_xrefs

    def _get_children(self, xrefs, func):

        return xrefs.get(func,[])

    def get_callers(self,func):

        return self._get_children(self.caller_xrefs,func)

    def get_callees(self,func):

        return self._get_children(self.callee_xrefs, func)


class NodeEncoder(json.JSONEncoder):
    '''
        Encodes nodes, the processed variable is used 
        to avoid circular references
    '''

    direction = 'callees'

    def __init__(self, *args, **kwargs):
    
        super(NodeEncoder, self).__init__(*args, **kwargs)
        self.processed = set()

    def default(self,object):

        if isinstance(object,Node):
            return self.encode_node(object)


    def encode_node(self,node):
        '''
            encode a node as a json object (can be used by d3)
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
            for child in getattr(node,self.direction):
                children.append(child)

            result = {  "name"      : node.name, 
                        "label"     : node.name,
                        "size"      : 1 ,
                        "sourcefile": node.sourcefile,
                        "type"      : "original",
                        "children"  : children
                     }

        return result


def get_all_funcs():
    '''
        Retrieve all functionss from the xref databases
    '''
    query = 'SELECT DISTINCT caller FROM xrefs'
    cursor  = con.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    result = [ x[0] for x in rows ]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Logging level (10: debug, 20 : info, etc )", default = logging.INFO, type = int)
    parser.add_argument("-r", "--callers", help="Export caller tree", action='store_true')
    parser.add_argument("-e", "--callees", help="Export caller tree", action='store_true')
    parser.add_argument("-a", "--allnodes", help="Dump all nodes", action='store_true')
    parser.add_argument("-d", "--directory", help="Output directory", default = '/tmp')
    parser.add_argument("nodes",nargs="*")
    args = parser.parse_args()
    if args.allnodes:
        # Dump everything
        # This still needs -r or -e to be specified
        nodenames = get_all_funcs()
        force = False
    else:
        nodenames = args.nodes
        force = True
    log.setLevel(args.verbose)
    log.debug(args)
    g = Graph()
    for noden in nodenames:
        node = g.add_node(noden)

    g.load(load_callers = args.callers, load_callees = args.callees)
    
    for node in nodenames:
        for direction in ( 'callers', 'callees' ):
            g.dump_node(node, args.directory , direction, force = force)    
    exit()


con = mdb.connect(DBHOST,DBUSER,DBPASS,DB)
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)


if __name__ == '__main__':
    main()
    
