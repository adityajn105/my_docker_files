# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: prediction_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import predict_pb2 as predict__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='prediction_service.proto',
  package='tensorflow.serving',
  syntax='proto3',
  serialized_options=_b('\370\001\001'),
  serialized_pb=_b('\n\x18prediction_service.proto\x12\x12tensorflow.serving\x1a\rpredict.proto2g\n\x11PredictionService\x12R\n\x07Predict\x12\".tensorflow.serving.PredictRequest\x1a#.tensorflow.serving.PredictResponseB\x03\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[predict__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_PREDICTIONSERVICE = _descriptor.ServiceDescriptor(
  name='PredictionService',
  full_name='tensorflow.serving.PredictionService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=63,
  serialized_end=166,
  methods=[
  _descriptor.MethodDescriptor(
    name='Predict',
    full_name='tensorflow.serving.PredictionService.Predict',
    index=0,
    containing_service=None,
    input_type=predict__pb2._PREDICTREQUEST,
    output_type=predict__pb2._PREDICTRESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PREDICTIONSERVICE)

DESCRIPTOR.services_by_name['PredictionService'] = _PREDICTIONSERVICE

# @@protoc_insertion_point(module_scope)
