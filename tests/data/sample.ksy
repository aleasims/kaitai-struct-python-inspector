meta:
  id: myform
  endian: le
  encoding: utf8
seq:
  - id: length
    type: u4
  - id: body
    type: str
    size: length
  - id: post
    type: mytype
    size-eos: true
types:
  mytype:
    seq:
      - id: field1
        type: u4
      - id: field2
        type: u4