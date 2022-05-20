# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: animus_common.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='animus_common.proto',
  package='animus.common',
  syntax='proto3',
  serialized_options=b'\n\035com.cyberselves.animus.commonB\021AnimusCommonProtoH\001Z%github.com/Cyberselves/AnimusMessages\242\002\014AnimusCommon\252\002\rAnimus.Common',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13\x61nimus_common.proto\x12\ranimus.common\";\n\x05\x45rror\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\"\x96\x01\n\x0bVersionInfo\x12\x13\n\x0b\x43oreVersion\x18\x01 \x01(\t\x12\x14\n\x0cRobotVersion\x18\x02 \x01(\t\x12\x15\n\rClientVersion\x18\x03 \x01(\t\x12\x16\n\x0e\x43lientLanguage\x18\x04 \x01(\t\x12\x15\n\rDriverVersion\x18\x05 \x01(\t\x12\x16\n\x0e\x44riverLanguage\x18\x06 \x01(\tBz\n\x1d\x63om.cyberselves.animus.commonB\x11\x41nimusCommonProtoH\x01Z%github.com/Cyberselves/AnimusMessages\xa2\x02\x0c\x41nimusCommon\xaa\x02\rAnimus.Commonb\x06proto3'
)




_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='animus.common.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='success', full_name='animus.common.Error.success', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='code', full_name='animus.common.Error.code', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='description', full_name='animus.common.Error.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=38,
  serialized_end=97,
)


_VERSIONINFO = _descriptor.Descriptor(
  name='VersionInfo',
  full_name='animus.common.VersionInfo',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='CoreVersion', full_name='animus.common.VersionInfo.CoreVersion', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='RobotVersion', full_name='animus.common.VersionInfo.RobotVersion', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ClientVersion', full_name='animus.common.VersionInfo.ClientVersion', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ClientLanguage', full_name='animus.common.VersionInfo.ClientLanguage', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='DriverVersion', full_name='animus.common.VersionInfo.DriverVersion', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='DriverLanguage', full_name='animus.common.VersionInfo.DriverLanguage', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
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
  serialized_start=100,
  serialized_end=250,
)

DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['VersionInfo'] = _VERSIONINFO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), {
  'DESCRIPTOR' : _ERROR,
  '__module__' : 'animus_common_pb2'
  # @@protoc_insertion_point(class_scope:animus.common.Error)
  })
_sym_db.RegisterMessage(Error)

VersionInfo = _reflection.GeneratedProtocolMessageType('VersionInfo', (_message.Message,), {
  'DESCRIPTOR' : _VERSIONINFO,
  '__module__' : 'animus_common_pb2'
  # @@protoc_insertion_point(class_scope:animus.common.VersionInfo)
  })
_sym_db.RegisterMessage(VersionInfo)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
