import numpy as np
import sys

import grpc
from grpc import RpcError

from protos.types_pb2 import DT_FLOAT
from protos.tensor_pb2 import TensorProto
from protos.tensor_shape_pb2 import TensorShapeProto
from protos.predict_pb2 import PredictRequest
from protos.prediction_service_pb2_grpc import PredictionServiceStub

def checkStatus(channel, timeout=10):
	try:
		grpc.channel_ready_future(channel).result(timeout=timeout)
		return True 
	except:
		return False

class CaptionPredictionService:
	def __init__(self, host:str = 'localhost', port:int = 8500 ):
		self.host_ip = f"{host}:{port}"
		self.channel = grpc.insecure_channel(self.host_ip)
		
		if checkStatus(self.channel):
			print('Connection Successful', file=sys.stdout)
		else:
			print('Connection Unsuccessful', file=sys.stderr)

		self.stub = PredictionServiceStub(self.channel)
		self.init_token = self.make_tensor_proto( np.array([[1]], dtype=np.float32) )
		self.init_h_c =  self.make_tensor_proto( np.zeros((1, 512), dtype=np.float32) )


	def make_tensor_proto(self, data):
	    # data should be a float32 numpy array
	    shape = data.shape
	    dims = [TensorShapeProto.Dim(size=i) for i in shape]
	    
	    proto_shape= TensorShapeProto(dim=dims)
	    proto_dtype = DT_FLOAT

	    tensor_proto = TensorProto(
	        dtype=proto_dtype,
	        tensor_shape=proto_shape)
	    tensor_proto.tensor_content = data.tostring()
	    return tensor_proto


	def predict(self, measurement, timeout=10):
		request = PredictRequest()
		request.model_spec.name = "caption_generator"
		request.inputs['input_1'].CopyFrom( self.make_tensor_proto( measurement.reshape(1, 224, 224, 3)).astype(np.float32) )
		request.inputs['input_5'].CopyFrom( self.init_token )
		request.inputs['input_2'].CopyFrom( self.init_h_c )
		request.inputs['input_3'].CopyFrom( self.init_h_c )

		try:
			response = self.stub.Predict(request, timeout=timeout)
			return np.array(response.outputs['stack_and_transpose'].float_val).reshape(20, 8063)
		except RpcError as err:
			print('Predict failed.', file=sys.stderr)
			print(err, file=sys.stderr)
			return None