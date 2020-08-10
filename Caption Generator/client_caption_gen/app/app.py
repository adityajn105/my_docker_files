"""
By - Aditya Jain
Contact - https://adityajain.me
Last Update - 3 Aug 2020
"""

from flask import Flask, render_template, request, jsonify, redirect
import base64
import numpy as np
import cv2
import os
import sys
from PIL import Image

from api import CaptionPredictionService

service = CaptionPredictionService( host=os.environ.get('TF_SERVER_IP', 'tf_server'), 
		port = int(os.environ.get('TF_SERVER_PORT', '8500')) )

idx2word = {}
idx = 0
with open('cap_gen_vocab.txt', 'r') as fp:
	for line in fp.readlines():
		word = line.strip()
		idx2word[idx] = word
		idx+=1
	print(f'Vocabulary of size {idx} loaded.', file=sys.stdout)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		image=request.files['image']
		image_string = base64.b64encode(image.read())
		
		binary = base64.b64decode(image_string)
		
		img = np.asarray(bytearray(binary), dtype="uint8")
		img = cv2.imdecode(img, 1)
		img = Image.fromarray(img)
		img = img.resize( (224,224), resample=Image.NEAREST )
		img = np.expand_dims(img, axis=0)
		img = np.flip(img, axis=-1)
		img = np.subtract( img, np.array([103.939, 116.779, 123.68]) )
		

		words = []
		nos = []
		for word in service.predict(img):
			word = np.argmax(word)
			nos.append(word)
			if word > 2: 
				words.append( idx2word[word] )
		print( " ".join(words), file=sys.stdout )
		print( nos, file=sys.stderr )
		return render_template('index.html', data={ 'status':True, 'img': str(image_string)[2:-1], 'caption': " ".join(words) })
	else:
		return render_template('index.html', data={ 'status':False })

if __name__== '__main__':
    app.run(host = '0.0.0.0', debug=True, port = int(80))