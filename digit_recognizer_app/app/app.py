from flask import Flask, render_template, request, jsonify, redirect
import base64
import numpy as np
import pickle as pkl
import cv2
import os
from predict import predict_digit
app = Flask(__name__)
stats = None

if not os.path.exists('stats/stats.pkl'):
    stats = { 'yes':0, 'no':0 }
    with open('stats/stats.pkl', 'wb') as fp:
        pkl.dump(stats,fp)


@app.route('/')
def home():
    acc = '100'
    with open('stats/stats.pkl', 'rb') as fp:
        global stats;
        stats = pkl.load(fp)
        total = sum(stats.values())
        if total!=0: acc = f"{ 100*stats['yes']/total:.2f} ({stats['yes']}/{total})"
    return render_template('index.html',data = {'status':False, 'accuracy':acc} ) 

@app.route('/charrecognize', methods = ['POST'])
def predict():
    if request.method == 'POST':
        data = request.get_json()
        imagebase64 = data['image']
        binary = base64.b64decode(imagebase64)
        img = np.asarray(bytearray(binary), dtype="uint8")
        img = 255-cv2.imdecode(img, 0)
        img = (cv2.resize(img, (20, 20))>127)*1
        final = np.zeros( (28,28) )
        final[ 4:24,4:24 ] = img
        final = final.reshape(1,28,28,1)
        return jsonify({
            'prediction': predict_digit(final),
            'status': True
        });

@app.route('/no', methods=['get'])
def no():
    with open('stats/stats.pkl', 'wb') as fp:
        stats['no']+=1
        pkl.dump(stats,fp)
    return redirect('/')

@app.route('/yes', methods=['get'])
def yes():
    with open('stats/stats.pkl', 'wb') as fp:
        stats['yes']+=1
        pkl.dump(stats,fp)
    return redirect('/')
        
if __name__=='__main__':
    app.run(host = '0.0.0.0',port = int(80))