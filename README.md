# KaitaiStruct Python Inspector (kspyspector)

[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![GitHub license](https://img.shields.io/github/license/aleasims/kaitai-struct-python-inspector)](https://github.com/aleasims/kaitai-struct-python-inspector/blob/master/LICENSE)


[Kaitai Struct project](https://github.com/kaitai-io)

This package contains tree builder for KaitaiStruct parsed objects.

Represents KaitaiStruct parsed Python objects as parse trees. Provides API to traverse it and store.

![](https://i.imgur.com/RapSXSH.png)

Analogue for [Kaitai Struct visualizer](https://github.com/kaitai-io/kaitai_struct_visualizer) 

## Requirements
* Python **>=3.5**

* KaitaiStruct Compiler **>=0.9**

  Use version from *unstable* branch (>=0.9), because it has bugs fixed! Install using `apt`:
  
  ```
  $ sudo apt-key adv --keyserver hkp://pool.sks-keyservers.net --recv 379CE192D401AB61
  $ echo "deb https://dl.bintray.com/kaitai-io/debian_unstable jessie main" | sudo tee /etc/apt/sources.list.d/kaitai.list
  $ sudo apt-get update
  $ sudo apt-get install kaitai-struct-compiler
  ```
  Ensure installation:
  ```
  $ ksc --version
  kaitai-struct-compiler 0.9-SNAPSHOT522603588
  ```

* Maybe you will need to install Java JDK. Easiest way using `apt`:

  ```
  sudo apt install openjdk-11-jdk
  ```

* Python virtual environment is recommended
  ```
  python3 -m venv env
  source env/bin/activate
  ```

* KaitaiStruct Python Runtime

  Compiler and runtime library versions should match! You`ve installed compiler from unstable branch and PyPi usually provides a stable version of runtime module. So it's better to install from source:
  ```
  git clone git@github.com:kaitai-io/kaitai_struct_python_runtime.git
  cd kaitai_struct_python_runtime
  pip install .
  ```

## Installation
Package itself can be installed using pip:
```
cd kspyspector
pip install .
```

Test that everything is done right:
```
kspyspector tests/data/sample.ksy tests/data/sample.bin
```

Installing in developers mode:
```
pip install -e .[dev]
```

## Guide

### CLI usage
After installation you can call inspector from shell:
```
$ kspyspector --help
usage: kspyspector [-h] [-v] [-V] [-e] [-o {dot,trawl}] [-f FILE]
                   ksy_file bin_file

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose
  -V, --version         show program's version number and exit

input:
  ksy_file              path to .ksy file
  bin_file              path to binary file

build flags:
  -e, --empty-ommit     do NOT include empty fields in result

output:
  -o {dot,trawl}, --output {dot,trawl}
                        serialize builded tree
  -f FILE, --file FILE  output to file (defaults to stdout)

example:
    kspyspector tests/data/sample.ksy tests/data/sample.bin
```

### API usage

You can simply call `Inspector`:
```python
ksy_file = 'path/to/ksy/file'
test_file = 'path/to/binary/file'

from inspector import Inspector

insp = Inspector(ksy_file, test_file)
```

Now parser is compiled, imported, data from `test_file` is parsed and tree is built. You can traverse builded tree:

```python
insp.tree.root.childs
# [magic(ValueNode<bytes>) [0:8], chunks(ArrayNode) [8:100], ...]
```

Usefull methods and fields of any ***nodes***:

* `name` — name of the node
* `childs` — ordered set of child nodes
* `parent` — parent node
* `raw_value` — corresponding source buffer slice
* `value` — interpreted value for `raw_value` *(exists only for ValueNodes!)*
* `start`, `end` — absolute segment addresses in buffer
* `size` — length of corresponding buffer slice

You can output builded tree in supported formats (extending):
```python
insp.to_trawl()
# {'Png': {'position': 0, 'offset': 0, 'length': 1156, 'type': 'ROOT', 'fields'...
insp.to_dot()
# 'digraph {\n\t"Png(RootNode) [0-1156]" -> "magic(ValueNode<bytes>) [0-8]"...
```


If you want to compile `.ksy` files yourself, you can do it:
```
ksc -t python --debug <your .ksy file>
```
But remind:
* Target language: **Python**
* `--debug` flag is required

Having `.ksy` compiled, you can invoke tree building:
```python
test_file = 'path/to/binary/file'

import parsetree
from myformat import Myformat

struct = Myformat.from_file(test_file)
struct._read()  # explicit call is required
tree = parsetree.build(struct)
```
or even shorter:
```python
tree = parsetree.parse_and_build(Myformat, test_file)
```
