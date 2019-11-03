# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: worker.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='worker.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0cworker.proto\"\x1f\n\x0emapper_request\x12\r\n\x05lines\x18\x01 \x03(\t\"#\n\x05tuple\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\")\n\x0fmapper_response\x12\x16\n\x06result\x18\x01 \x03(\x0b\x32\x06.tuple\"\x1c\n\x0cping_request\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1d\n\rping_response\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"j\n\x10reducer_response\x12)\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1b.reducer_response.DataEntry\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"h\n\x0freducer_request\x12(\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\x1a.reducer_request.DataEntry\x1a+\n\tDataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\x9d\x01\n\x06Worker\x12\'\n\x04ping\x12\r.ping_request\x1a\x0e.ping_response\"\x00\x12\x31\n\nworker_map\x12\x0f.mapper_request\x1a\x10.mapper_response\"\x00\x12\x37\n\x0eworker_reducer\x12\x10.reducer_request\x1a\x11.reducer_response\"\x00\x62\x06proto3')
)




_MAPPER_REQUEST = _descriptor.Descriptor(
  name='mapper_request',
  full_name='mapper_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lines', full_name='mapper_request.lines', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=47,
)


_TUPLE = _descriptor.Descriptor(
  name='tuple',
  full_name='tuple',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tuple.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tuple.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=84,
)


_MAPPER_RESPONSE = _descriptor.Descriptor(
  name='mapper_response',
  full_name='mapper_response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='result', full_name='mapper_response.result', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=86,
  serialized_end=127,
)


_PING_REQUEST = _descriptor.Descriptor(
  name='ping_request',
  full_name='ping_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='ping_request.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=129,
  serialized_end=157,
)


_PING_RESPONSE = _descriptor.Descriptor(
  name='ping_response',
  full_name='ping_response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='ping_response.data', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=159,
  serialized_end=188,
)


_REDUCER_RESPONSE_DATAENTRY = _descriptor.Descriptor(
  name='DataEntry',
  full_name='reducer_response.DataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='reducer_response.DataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='reducer_response.DataEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=253,
  serialized_end=296,
)

_REDUCER_RESPONSE = _descriptor.Descriptor(
  name='reducer_response',
  full_name='reducer_response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='reducer_response.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_REDUCER_RESPONSE_DATAENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=190,
  serialized_end=296,
)


_REDUCER_REQUEST_DATAENTRY = _descriptor.Descriptor(
  name='DataEntry',
  full_name='reducer_request.DataEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='reducer_request.DataEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='reducer_request.DataEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=253,
  serialized_end=296,
)

_REDUCER_REQUEST = _descriptor.Descriptor(
  name='reducer_request',
  full_name='reducer_request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='reducer_request.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_REDUCER_REQUEST_DATAENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=298,
  serialized_end=402,
)

_MAPPER_RESPONSE.fields_by_name['result'].message_type = _TUPLE
_REDUCER_RESPONSE_DATAENTRY.containing_type = _REDUCER_RESPONSE
_REDUCER_RESPONSE.fields_by_name['data'].message_type = _REDUCER_RESPONSE_DATAENTRY
_REDUCER_REQUEST_DATAENTRY.containing_type = _REDUCER_REQUEST
_REDUCER_REQUEST.fields_by_name['data'].message_type = _REDUCER_REQUEST_DATAENTRY
DESCRIPTOR.message_types_by_name['mapper_request'] = _MAPPER_REQUEST
DESCRIPTOR.message_types_by_name['tuple'] = _TUPLE
DESCRIPTOR.message_types_by_name['mapper_response'] = _MAPPER_RESPONSE
DESCRIPTOR.message_types_by_name['ping_request'] = _PING_REQUEST
DESCRIPTOR.message_types_by_name['ping_response'] = _PING_RESPONSE
DESCRIPTOR.message_types_by_name['reducer_response'] = _REDUCER_RESPONSE
DESCRIPTOR.message_types_by_name['reducer_request'] = _REDUCER_REQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

mapper_request = _reflection.GeneratedProtocolMessageType('mapper_request', (_message.Message,), {
  'DESCRIPTOR' : _MAPPER_REQUEST,
  '__module__' : 'worker_pb2'
  # @@protoc_insertion_point(class_scope:mapper_request)
  })
_sym_db.RegisterMessage(mapper_request)

tuple = _reflection.GeneratedProtocolMessageType('tuple', (_message.Message,), {
  'DESCRIPTOR' : _TUPLE,
  '__module__' : 'worker_pb2'
  # @@protoc_insertion_point(class_scope:tuple)
  })
_sym_db.RegisterMessage(tuple)

mapper_response = _reflection.GeneratedProtocolMessageType('mapper_response', (_message.Message,), {
  'DESCRIPTOR' : _MAPPER_RESPONSE,
  '__module__' : 'worker_pb2'
  # @@protoc_insertion_point(class_scope:mapper_response)
  })
_sym_db.RegisterMessage(mapper_response)

ping_request = _reflection.GeneratedProtocolMessageType('ping_request', (_message.Message,), {
  'DESCRIPTOR' : _PING_REQUEST,
  '__module__' : 'worker_pb2'
  # @@protoc_insertion_point(class_scope:ping_request)
  })
_sym_db.RegisterMessage(ping_request)

ping_response = _reflection.GeneratedProtocolMessageType('ping_response', (_message.Message,), {
  'DESCRIPTOR' : _PING_RESPONSE,
  '__module__' : 'worker_pb2'
  # @@protoc_insertion_point(class_scope:ping_response)
  })
_sym_db.RegisterMessage(ping_response)

reducer_response = _reflection.GeneratedProtocolMessageType('reducer_response', (_message.Message,), {

  'DataEntry' : _reflection.GeneratedProtocolMessageType('DataEntry', (_message.Message,), {
    'DESCRIPTOR' : _REDUCER_RESPONSE_DATAENTRY,
    '__module__' : 'worker_pb2'
    # @@protoc_insertion_point(class_scope:reducer_response.DataEntry)
    })
  ,
  'DESCRIPTOR' : _REDUCER_RESPONSE,
  '__module__' : 'worker_pb2'
  # @@protoc_insertion_point(class_scope:reducer_response)
  })
_sym_db.RegisterMessage(reducer_response)
_sym_db.RegisterMessage(reducer_response.DataEntry)

reducer_request = _reflection.GeneratedProtocolMessageType('reducer_request', (_message.Message,), {

  'DataEntry' : _reflection.GeneratedProtocolMessageType('DataEntry', (_message.Message,), {
    'DESCRIPTOR' : _REDUCER_REQUEST_DATAENTRY,
    '__module__' : 'worker_pb2'
    # @@protoc_insertion_point(class_scope:reducer_request.DataEntry)
    })
  ,
  'DESCRIPTOR' : _REDUCER_REQUEST,
  '__module__' : 'worker_pb2'
  # @@protoc_insertion_point(class_scope:reducer_request)
  })
_sym_db.RegisterMessage(reducer_request)
_sym_db.RegisterMessage(reducer_request.DataEntry)


_REDUCER_RESPONSE_DATAENTRY._options = None
_REDUCER_REQUEST_DATAENTRY._options = None

_WORKER = _descriptor.ServiceDescriptor(
  name='Worker',
  full_name='Worker',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=405,
  serialized_end=562,
  methods=[
  _descriptor.MethodDescriptor(
    name='ping',
    full_name='Worker.ping',
    index=0,
    containing_service=None,
    input_type=_PING_REQUEST,
    output_type=_PING_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='worker_map',
    full_name='Worker.worker_map',
    index=1,
    containing_service=None,
    input_type=_MAPPER_REQUEST,
    output_type=_MAPPER_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='worker_reducer',
    full_name='Worker.worker_reducer',
    index=2,
    containing_service=None,
    input_type=_REDUCER_REQUEST,
    output_type=_REDUCER_RESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_WORKER)

DESCRIPTOR.services_by_name['Worker'] = _WORKER

# @@protoc_insertion_point(module_scope)
