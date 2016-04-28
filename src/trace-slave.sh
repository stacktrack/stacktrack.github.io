#!/bin/bash
#
# trinity is our test program.
# We use gdb because the kernel gdb session creates TRAP breakpoints which we 
# must ignore
#
cd /mnt/t/trinity
gdb -q -x /mnt/t/gdbcmds-slave trinity
