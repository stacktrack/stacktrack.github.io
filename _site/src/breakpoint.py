#

'''

set pagination off
target remote u:8864

python
breakpoint.del_bps()
end

python

import breakpoint, importlib
importlib.reload(breakpoint)
breakpoint.STBreakpoint('sys_chdir')

end

c

python
STBreakpoint.graph.dump_nodes('/tmp')
end

'''

import gdb
import linux
import sys
import MySQLdb as mdb
import json
from Graph import *


def get_callees(symbol):
    return  g.xrefdb.get_callees(symbol)
    
    

def del_bps(start=None,end=None):
    for bp in gdb.breakpoints():
        bp.delete()

def get_current():
    lxc=linux.cpus.LxCurrentFunc()
    return lxc.invoke()

def get_bt_start():
    backtrace = gdb.execute('backtrace', to_string = True)
    # 
    # #4  0xffffffff817be132 in entry_SYSCALL_64_fastpath
    f_end    = backtrace.split('\n')[-3].split(' ')[2]
    print(backtrace)
    print('fend: {}'.format(f_end))
    EndBreakPoint(f_end)

class EndBreakPoint(gdb.Breakpoint):
    
    def __init__(self,address):
        func_name = '*' + address
        print('ENDBP at '+ func_name) 
        super(EndBreakPoint, self).__init__(
            func_name, gdb.BP_BREAKPOINT, internal=False
        )

    def stop(self):
        comm = get_current()['comm'].string()
        if not comm.startswith('trinity'):
            return
        print('Finalizing trace')
        for bp in gdb.breakpoints():
            if bp == self:
                bp.enabled = False
            else:
                bp.delete()
        STBreakpoint.graph.dump_nodes('/tmp')
        print('DONE')
        print(dir(self))



class STBreakpoint(gdb.Breakpoint):

    bplist   = set()
    todelete = []
    edges    = []
    graph    = Graph()

    def __init__(self, func_name, parent=None):

        self.func_name = func_name        
        # node = self.node      = self.graph.add_node(func_name)
        # if not node in self.graph.nodes: self.graph.load_node(self.node)
        self.parent    = parent
        STBreakpoint.bplist.add(func_name)
        #print('ini %s'%str(func_name))
        super(STBreakpoint, self).__init__(
            func_name, gdb.BP_BREAKPOINT, internal=False
        )
 
    def _stop(self):
        comm = get_current()['comm'].string()
        if not comm.startswith('trinity'):
            return
        print(self.func_name)

    def stop(self):
        comm = get_current()['comm'].string()
        if not comm.startswith('trinity'):
            return
       
        if self.parent:
            STBreakpoint.graph.add_edge(self.parent,self.func_name)
        else:
            get_bt_start()


        for bp in STBreakpoint.todelete:
            try:
                if bp.func_name != self.func_name:
                    bp.delete()
            except:
                pass
      
        for callee in get_callees(self.func_name):
            if callee not in STBreakpoint.bplist:
                STBreakpoint(callee,self.func_name)

        STBreakpoint.todelete += [self]
        #self.delete()
        

symbol = 'sys_chdir'
g = Graph()
node = g.add_node(symbol)
print('loading {}'.format(node))
g.load(load_callers = False, load_callees = True)


