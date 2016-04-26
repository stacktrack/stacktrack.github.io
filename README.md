stacktrack.github.io
=====================

## Quick Start

Clone repository

```
git clone git@github.com:stacktrack/stacktrack.github.com.git
cd stacktrack.github.com
```

Load database 

```
mysql stacktrack < database/stacktrack.sql
```

Generate a graph
```
python src/Graph.py tun_get_user -r -e
```

Usage

```

usage: Graph.py [-h] [-v VERBOSE] [-r] [-e] [-a] [-d DIRECTORY]
                [nodes [nodes ...]]

positional arguments:
  nodes

optional arguments:
  -h, --help            show this help message and exit
  -v VERBOSE, --verbose VERBOSE
                        Logging level (10: debug, 20 : info, etc )
  -r, --callers         Export caller tree
  -e, --callees         Export caller tree
  -a, --allnodes        Dump all nodes
  -d DIRECTORY, --directory DIRECTORY
                        Output directory

```

## Content Description

+ The root folder contains all the files used to render the web interface on stacktrack.github.io

+ The src directory contains the source code used to create the json graphs

+ The database directory contains a dump of the xref database

## Setup 

In order to create your own graphs you need the following setup:

+ Linux server with virsh, gdb, samba, mysql
+ Guest vm with a kernel compiled with debug symbols
+ The database needs to be loaded and Graph.py must be able to create graphs
