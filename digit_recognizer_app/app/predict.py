import CNNModel
import numpy as np
model = CNNModel.build('saved_weights/CNN_mnist_weights.h5')

def predict_digit(img):
    onehot = model.predict(img)[0]
    no = np.argmax(onehot)
    prob = onehot[no]
    return f"{no} | Confidence: {prob}"