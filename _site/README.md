stacktrack.github.io
=====================

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
