# kaitai-struct-python-inspector
Tree builder for KaitaiStruct parsed objects.

Represents KaitaiStruct parsed Python objects as parse trees. Provides API to traverse it.

Shout out to [Kaitai team](https://github.com/kaitai-io) :)

## Requirements
* **Python3.6**
* `kaitaistruct`
* `pydotplus` *(not necessary for API)*

```
pip install -r requirements.txt
```

## Guide
### CLI example
TODO

### API example

You can call `Inspector`:
```python
ksy_file = 'path/to/ksy/file'
test_file = 'path/to/binary/file'

from inspector import Inspector

insp = Inspector(ksy_file, test_file)
```

Now you can traverse builded tree:

```python
insp.tree.root.childs
# [magic(ValueNode<bytes>) [0:8], chunks(ArrayNode) [8:100], ...]
```

Usefull methods and fields:

* `name` — name of the node
* `childs` — ordered set of child nodes
* `parent` — parent node
* `raw_value` — corresponding source buffer slice
* `value` — interpreted value for `raw_value` *(exists only for ValueNodes!)*
* `start`, `end` — absolute segment addresses in buffer


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
struct._read()
tree = parsetree.build(struct)
```
or even shorter:
```python
tree = parsetree.parse_and_build(Myformat, test_file)
```
