#!/bin/bash
#
# This script creates a trace as follows:
#   - Reset the VM snapshot
#   - create gdb command files to be run on the master and the slave (VM)
#   - start gdb on the master
#   - ssh to the slave and start the test (trace-slave.sh)
#
# The gdb session on the master will set a breakpoint on SYSCALL (argv[1]).
# When the breakpoint is hit by the program on the slave, nodes are added to
# the trace. When the program exits, the nodes are dumped.
#

SYSCALL=$1
VM=192.168.122.10

if [[ -z $SYSCALL ]]
then
    echo no syscall
    exit 1
fi

virsh snapshot-revert tvm tvm-0

GDBCMDS_MASTER=$(mktemp)
GDBCMDS_SLAVE=/mnt/t/gdbcmds-slave

sed -e "s/_SYSCALL_/sys_$SYSCALL/g" gdbcmds > $GDBCMDS_MASTER
sed -e "s/_SYSCALL_/$SYSCALL/g" gdbcmds-client > $GDBCMDS_SLAVE

gdb -q -x $GDBCMDS_MASTER & 
PID_GDB=$!

sleep 20
ssh root@$VM /mnt/t/trace-slave.sh &
PID_SSH=$!

(sleep 1800 ; kill -9 $PID_GDB $PID_SSH) &

wait $PID_SSH

rm -f $GDBCMDS_MASTER $GDBCMDS_SLAVE
