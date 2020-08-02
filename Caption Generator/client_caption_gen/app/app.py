"""
By - Aditya Jain
Contact - https://adityajain.me
Last Update - 3 Aug 2020
"""

# https://grpc.io/docs/languages/python/quickstart/
# https://stackoverflow.com/questions/55033952/grpc-only-tensorflow-serving-client-in-c

from flask import Flask, render_template, request, jsonify, redirect
import base64
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

import grpc
from grpc import RpcError

from proto.types_pb2 import DT_FLOAT
from proto.tensor_pb2 import TensorProto
from proto.tensor_shape_pb2 import TensorShapeProto
from proto.predict_pb2 import PredictRequest
from proto.prediction_service_pb2_grpc import PredictionServiceStub


app = Flask(__name__)

class PredictionService:
	def __init__(self, host:str = 'localhost', port:int = 8500 ):
		self.host_ip = f"{host}:{port}"
		self.channel = grpc.insecure_channel(self.host_ip)
		self.stub = PredictionServiceStub(self.channel)

	def tensor_proto_from_measurement(self, measurement):
        """Pass in a measurement and return a tensor_proto protobuf object"""
        return TensorProto(
            dtype=self.dtype,
            tensor_shape=TensorShapeProto(dim=self.dims),
            string_val=[bytes(measurement)])

    def predict(self, measurement, timeout=10):
        """Execute prediction against TF Serving service"""
        request = PredictRequest()
        request.model_spec.name = "caption_generator"

        request.inputs['inputs'].CopyFrom(
            self.tensor_proto_from_measurement(measurement))

        try:
            return self.stub.Predict(request, timeout=timeout)
        except RpcError as err:
            print('Predict failed.')
            print(err)
            return None



@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		image=request.files['image']
		image_string = base64.b64encode(image.read())
		
		binary = base64.b64decode(image_string)
		img = np.asarray(bytearray(binary), dtype="uint8")
		img = cv2.imdecode(img, 1)
		img = cv2.resize( img, (224,224), interpolation=cv2.INTER_AREA )

		return render_template('index.html', data={ 'status':True, 'img': str(image_string)[2:-1], 'caption': "This is app is under training progress."})
	else:
		return render_template('index.html', data={ 'status':False })

if __name__== '__main__':
    app.run(host = '0.0.0.0', debug=True, port = int(5000))