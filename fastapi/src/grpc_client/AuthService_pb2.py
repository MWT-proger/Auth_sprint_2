# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: AuthService.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11\x41uthService.proto\x12\x04role\"!\n\x0b\x41uthRequest\x12\x12\n\naccess_key\x18\x01 \x01(\t\"!\n\x0c\x41uthResponse\x12\x11\n\tuser_role\x18\x01 \x03(\t2>\n\x04\x41uth\x12\x36\n\x0bGetUserRole\x12\x11.role.AuthRequest\x1a\x12.role.AuthResponse\"\x00\x62\x06proto3')



_AUTHREQUEST = DESCRIPTOR.message_types_by_name['AuthRequest']
_AUTHRESPONSE = DESCRIPTOR.message_types_by_name['AuthResponse']
AuthRequest = _reflection.GeneratedProtocolMessageType('AuthRequest', (_message.Message,), {
  'DESCRIPTOR' : _AUTHREQUEST,
  '__module__' : 'AuthService_pb2'
  # @@protoc_insertion_point(class_scope:role.AuthRequest)
  })
_sym_db.RegisterMessage(AuthRequest)

AuthResponse = _reflection.GeneratedProtocolMessageType('AuthResponse', (_message.Message,), {
  'DESCRIPTOR' : _AUTHRESPONSE,
  '__module__' : 'AuthService_pb2'
  # @@protoc_insertion_point(class_scope:role.AuthResponse)
  })
_sym_db.RegisterMessage(AuthResponse)

_AUTH = DESCRIPTOR.services_by_name['Auth']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _AUTHREQUEST._serialized_start=27
  _AUTHREQUEST._serialized_end=60
  _AUTHRESPONSE._serialized_start=62
  _AUTHRESPONSE._serialized_end=95
  _AUTH._serialized_start=97
  _AUTH._serialized_end=159
# @@protoc_insertion_point(module_scope)
