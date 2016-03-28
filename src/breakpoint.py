#

'''

set pagination off
target remote u:8864

python
breakpoint.del_bps()
end



python
from Graph import *
import importlib, breakpoint
importlib.reload(breakpoint)
breakpoint.KxrBreakpoint('sys_chdir')
end



python
KxrBreakpoint.graph.dump_nodes('/tmp')
end

'''

import gdb
import linux
import sys
import MySQLdb as mdb
import json
import importlib
from Graph import *


def get_callees(symbol):
    return g.xrefdb.get_callees(symbol)

def del_bps(start=None,end=None):
    for bp in gdb.breakpoints():
        bp.delete()

def get_current():
    lxc=linux.cpus.LxCurrentFunc()
    return lxc.invoke()

class KxrBreakpoint(gdb.Breakpoint):

    bplist   = set()
    todelete = []
    edges    = []
    graph    = Graph()

    def __init__(self, func_name, parent=None):

        self.func_name = func_name        
        print(func_name)
        # node = self.node      = self.graph.add_node(func_name)
        # if not node in self.graph.nodes: self.graph.load_node(self.node)
        self.parent    = parent
        KxrBreakpoint.bplist.add(func_name)
        # print('ini %s'%str(func_name))
        super(KxrBreakpoint, self).__init__(
            func_name, gdb.BP_BREAKPOINT, internal=False
        )
 
    def stop(self):
        comm = get_current()['comm'].string()
        if not comm.startswith('trinity'):
            return
        
        if self.parent:
            KxrBreakpoint.graph.add_edge(self.parent,self.func_name)

        for bp in KxrBreakpoint.todelete:
            try:
                if bp.func_name != self.func_name:
                    bp.delete()
            except:
                pass
      
        
        #callees = [ c.name for c in self.node.get_callees()]

        for callee in get_callees(self.func_name):
            self.edges += [(self.func_name,callee)]
            if callee not in KxrBreakpoint.bplist:
                KxrBreakpoint(callee,self.func_name)

        KxrBreakpoint.todelete += [self]
        #gdb.execute('continue')
        #self.delete()
        

symbol = 'sys_chdir'
print('loading '+symbol)
g = Graph()
node = g.add_node(symbol)
g.load(load_callers = False, load_callees = True)
print('loaded')

