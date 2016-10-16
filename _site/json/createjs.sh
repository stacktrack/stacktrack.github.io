#!/bin/bash
(
cd json
echo 'var syscalls = ['
ls | grep race | while read line
do
    syscall=$(echo $line | cut -f2- -d_ | cut -f1 -d- | sed -e 's/_callees//g')
    echo "['$syscall','$line'],"
done

echo '];') > /var/u/stacktrack.github.com/js/traces.js
