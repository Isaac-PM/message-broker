# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protocol.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0eprotocol.proto\x12\x08protocol\"\\\n\rSesionRequest\x12\x0c\n\x04tipo\x18\x01 \x01(\x05\x12\x11\n\tidUsuario\x18\x02 \x01(\t\x12\x13\n\x0btipoUsuario\x18\x03 \x01(\x05\x12\x15\n\rsuscripciones\x18\x04 \x01(\t\" \n\x0eSesionResponse\x12\x0e\n\x06\x65stado\x18\x01 \x01(\x05\"c\n\x0eMensajeRequest\x12\x15\n\ridentificador\x18\x01 \x01(\t\x12\x0e\n\x06idTema\x18\x02 \x01(\x05\x12\x17\n\x0fidUsuarioEmisor\x18\x03 \x01(\t\x12\x11\n\tcontenido\x18\x04 \x01(\t\"Q\n\x0fMensajeResponse\x12\x15\n\ridentificador\x18\x01 \x01(\t\x12\x17\n\x0fidUsuarioEmisor\x18\x02 \x01(\t\x12\x0e\n\x06\x65stado\x18\x03 \x01(\x05\x32\x90\x01\n\x07Mensaje\x12=\n\x06sesion\x12\x17.protocol.SesionRequest\x1a\x18.protocol.SesionResponse\"\x00\x12\x46\n\renviarMensaje\x12\x18.protocol.MensajeRequest\x1a\x19.protocol.MensajeResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protocol_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SESIONREQUEST._serialized_start=28
  _SESIONREQUEST._serialized_end=120
  _SESIONRESPONSE._serialized_start=122
  _SESIONRESPONSE._serialized_end=154
  _MENSAJEREQUEST._serialized_start=156
  _MENSAJEREQUEST._serialized_end=255
  _MENSAJERESPONSE._serialized_start=257
  _MENSAJERESPONSE._serialized_end=338
  _MENSAJE._serialized_start=341
  _MENSAJE._serialized_end=485
# @@protoc_insertion_point(module_scope)
