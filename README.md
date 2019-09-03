# KaitaiStruct Python Inspector (kspyspector)

[![Python 3.5](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/release/python-350/)
[![GitHub license](https://img.shields.io/github/license/aleasims/kaitai-struct-python-inspector)](https://github.com/aleasims/kaitai-struct-python-inspector/blob/master/LICENSE)


[Kaitai Struct project](https://github.com/kaitai-io)

This package contains tree builder for KaitaiStruct parsed objects.

Represents KaitaiStruct parsed Python objects as parse trees. Provides API to traverse it and store.

![](https://i.imgur.com/RapSXSH.png)

Analogue for [Kaitai Struct visualizer](https://github.com/kaitai-io/kaitai_struct_visualizer) 

## Requirements
* **Python3.5**
* `kaitai-struct-compiler` ([install](http://kaitai.io/#download))

***Pay attention:*** compiler and runtime library versions should match! If you install *unstable* version of compiler, you would probably need to install runtime library from source:
```
git clone git@github.com:kaitai-io/kaitai_struct_python_runtime.git
cd kaitai_struct_python_runtime
pip install .
```

## Installation
It's recommended to install everything into virtual environment.

You can install package using pip:
```
cd kspyspector
pip install .
```

## Guide

### CLI usage
After installation you can call inspector from shell:
```
kspyspector --help
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
