#!/bin/bash

#exec_slave(){
alias sshu="ssh 'root@192.168.122.10'"

SYSCALL=$1

if [[ -z $SYSCALL ]]
then
    echo no syscall
    exit 1
fi

virsh snapshot-revert tvm tvm-0

GDBCMDS_MASTER=$(mktemp)
GDBCMDS_SLAVE=/mnt/t/gdbcmds-client

sed -e "s/_SYSCALL_/sys_$SYSCALL/g" gdbcmds > $GDBCMDS_MASTER
sed -e "s/_SYSCALL_/$SYSCALL/g" gdbcmds-client > $GDBCMDS_SLAVE

gdb -q -x $GDBCMDS_MASTER & 
PID_GDB=$!

sleep 20
ssh 'root@192.168.122.10' /mnt/t/trace-client.sh &
PID_SSH=$!

(sleep 1800 ; kill -9 $PID_GDB $PID_SSH) &

wait $PID_SSH

#sshu cat /mnt/log
#killall -9 gdb

rm -f $GDBCMDS_MASTER $GDBCMDS_SLAVE
