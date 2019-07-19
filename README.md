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

## Example usage
### CLI example
TODO

### API example
Compile with `ksc` any `.ksy` file:
```
ksc -t python --debug <your .ksy file>
```

* Target language: **Python**
* `--debug` required!

You can call `Inspector`:
```python
ksy_file = 'path/to/ksy/file'
test_file = 'path/to/binary/file'

from inspector import Inspector

insp = Inspector(ksy_file, test_file)
```


Or you can directly invoke nodes creating:
```python
test_file = 'path/to/binary/file'

from parsetree import RootNode
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

* `childs` — ordered set of childs of the node
* `parent` — parent of the node
* `raw_value` — corresponding buffer slice
* `value` — interpreted value for `raw_value` *(exists only for ValueNodes!)*
* `start`, `end` — absolute segment addresses in buffer
