# Stacktrack Src Readme

This directory contains the code to create the json files (callgraphs and execution traces): 
+ Static Call graphs are created with the Graph.py which queries the xref database
+ Dynamic call graphs (which I call execution traces) are created with the trace.sh script. The tracing sets kernel breakpoints on the master. It then ssh's to the slave to execute the test program on the slave. 

## Installation

To install the xref database and query it to generate call graphs in json format, execute the following commands:

```
git clone https://github.com/stacktrack/stacktrack.github.com
cd stacktrack.github.com/
mysql -e "create database stacktrack"
mysql stacktrack < database/stacktrack.sql
# Change database username & password (DBUSER & DBPASS) in 
vi src/Graph.py
python src/Graph.py -e sys_kexec_file_load
```

You will need python 2.7, and MySQL-python. 

```
$ python src/Graph.py -e sys_kexec_file_load
INFO:root:dumping callees of Node sys_kexec_file_load to /tmp/sys_kexec_file_load_callees.json
```

The json graphs can be rendered with the tree.html html code in the repository by adding adding a 'json=' url parameter. For example

http://stacktrack.github.io/tree.html?json=sys_kexec_file_load_callees.json

The javascript graph rendering is done in javascript so it can run locally.

