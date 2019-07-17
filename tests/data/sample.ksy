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
    type: str
    size-eos: true
