# kaitai-struct-python-inspector
Inspector for KaitaiStruct parsed objects.

Represents KaitaiStruct persed objects (in Python) as trees. Provides API to traverse it.

Shout out to [Kaitai team](https://github.com/kaitai-io) :)

## Requirements
* **Python3.6**
* `kaitaistruct`
```
pip install kaitaistruct
```

## Example usage
Compile with `ksc` any `.ksy` file:
```
ksc -t python --debug <your .ksy file>
```

**Important:**
* Target language: **Python**
* `--debug` required!

Usage:
```python
test_file = 'path/to/binary/file'

from parsertree import RootNode
# Your compiled parser
from myformat import Myformat

parser = Myformat.from_file(test_file)
# Required to call `read` manually, because of `--debug`
parser._read()

with open(test_file, 'rb') as f:
    buffer = f.read()

tree = RootNode(buffer, parser)
```

Now you can traverse builded tree!

Usable methods and fileds:

* `childs`
* `parent`
* `raw_value`
* `value` *(only for ValueNodes)*
* `start`, `end` *(right now are broken for substreams cases)*
