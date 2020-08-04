
python -m grpc_tools.protoc -I=protos --python_out=../app/protos  types.proto 

python -m grpc_tools.protoc -I=protos --python_out=../app/protos  resource_handle.proto 

python -m grpc_tools.protoc -I=protos --python_out=../app/protos  tensor.proto 

python -m grpc_tools.protoc -I=protos --python_out=../app/protos  model.proto 

python -m grpc_tools.protoc -I=protos --python_out=../app/protos  tensor_shape.proto 

python -m grpc_tools.protoc -I=protos --python_out=../app/protos  predict.proto 

python -m grpc_tools.protoc -I=protos --python_out=../app/protos  wrappers.proto 

python -m grpc_tools.protoc -I=protos --python_out=../app/protos --grpc_python_out=../app/protos prediction_service.proto 