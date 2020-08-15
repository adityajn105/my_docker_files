import pandas as pd
import numpy as np
import cv2

import os
import time

import pickle as pkl

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.optimizers import Adam, RMSprop

print(tf.__version__)

from models import Model


result = pd.read_csv('captions.txt', engine='c')
result['len'] = result.caption.apply( lambda x: len(str(x).split()) )
result = result[ result.len < np.percentile(result.len, 95) ]
print(result.shape)
print(result.head())


def preprocess_comment(x):
  x = str(x).lower()
  to_replace = { "'s": " 's", "'ve": " have", "'re": " are", '-':' ' }
  x = str(x)
  for k,v in to_replace.items():
    x = x.replace( k, v )
  x = "".join([ c for c in x if c.isalpha() or c==" " ])
  x = " ".join([ w for w in x.split() if len(w)>1 ])
  return x
result.caption = result.caption.apply(preprocess_comment)
print(result.head(2))

words = { '<pad>', '<sos>', '<eos>' }
for caption in result.caption.values:
  for word in caption.split():
    words.add(word)
words = sorted(list(words))
VOCAB_SIZE = len(words)
print('VOCAB_SIZE', VOCAB_SIZE)


EMBEDDING_DIM = 50
## Preparing GLove word embedding and embedding_matrix
word2idx = {'<pad>': 0, '<sos>':1, '<eos>':2}
idx2word = {0:'<pad>', 1: '<sos>', 2: '<eos>' }
i=3
for word in words:
  if word in ('<pad>', '<eos>', '<sos>'): continue
  word2idx[word] = i
  idx2word[i] = word
  i+=1

#save all vocabulary
pd.DataFrame( list(word2idx.keys()) ).to_csv('cap_gen_vocab.txt', index=False, header=False)

glove_dict = { '<pad>': [0]*50, '<sos>':[0]*50, '<eos>':[0]*50 } 
with open('glove.6B.50d.txt', "r") as fp:
  for line in fp.readlines():
    a = line.split()
    glove_dict[a[0].lower()] = np.array(list(map(float, a[1:])))


embedding_matrix = np.zeros( (VOCAB_SIZE, 50) )
unknowns=set()
for word,idx in word2idx.items():
  if word not in glove_dict:
    unknowns.add(word)
    embedding_matrix[idx] = glove_dict['unk']
  else:
    embedding_matrix[idx] = glove_dict[word]
print(embedding_matrix.shape)
print("Total Unknowns", len(unknowns))

MAX_LEN = 20
def encode_sequence( x, mlen=MAX_LEN, pad='post', pad_value=0):
  x = np.array([ word2idx[w] for w in x.split()+['<eos>']], dtype=np.int32)
  if len(x) > mlen: return x[:mlen]
  else: 
    res = np.zeros(mlen, dtype=np.int32)
    res[:len(x)] = x
    return res

#for teacher forcing
def encode_sequence_tf( x, mlen=MAX_LEN, pad='post', pad_value=0):
  x = np.array([ word2idx[w] for w in x.split()], dtype=np.int32)
  if len(x) > mlen: return x[:mlen]
  else: 
    res = np.zeros(mlen, dtype=np.int32)
    res[:len(x)] = x
    return res
y = result.caption.apply( lambda x: encode_sequence(x) ).values
ytf = result.caption.apply( lambda x: encode_sequence_tf(x) ).values

size = int(len(y)*.8)
x_train, x_val, y_train, y_val, ytf_train, ytf_val =  train_test_split( result.image.values, y, ytf, test_size=0.25 )
print(x_train.shape, y_train.shape, ytf_train.shape, x_val.shape)


#preprocessing to get input for vgg19
def vgg19_preprocess_input(x):
  x = x[..., ::-1] #RGB to BGR
  return np.subtract( x, np.array([103.939, 116.779, 123.68]) )

#defining batch generator
def batch_generator( x, y, ytf, batch_size = 128 ):
  n_batches = len(x)//batch_size
  for i in range( n_batches ):
    X =  np.empty( (0,224,224,3) )
    for img in x[i*batch_size : (i+1)*batch_size]:
      img = np.flip(cv2.imread( f"Images/{img}"), axis=-1) #BGR to RGB
      img = Image.fromarray(img)
      img = img.resize((224, 224), resample = Image.NEAREST)
      img = np.expand_dims( img, axis=0 )
      img = vgg19_preprocess_input(img)
      X = np.concatenate( (X, img) )

    ys = y[i*batch_size : (i+1)*batch_size]
    Y = np.zeros( (len(ys), MAX_LEN, VOCAB_SIZE) )
    for j in range(len(ys)):
      for k in range(MAX_LEN):
        token = ys[j][k]
        Y[j][k][token] = 1

    Ytf = np.empty( (0, MAX_LEN) )
    for j in range(len(ys)):
      Ytf = np.concatenate( (Ytf, np.expand_dims(ytf[j], axis=0)) )

    inital_hc = np.zeros( (len(ys), 512) )
    yield  [ X, Ytf, inital_hc, inital_hc ], Y

#custom acc because we dont want to consider padding
def acc(y_true, y_pred):
  # both are of shape ( _, Ty, VOCAB_SIZE )
  targ = K.argmax(y_true, axis=-1)
  pred = K.argmax(y_pred, axis=-1)
  correct = K.cast(  K.equal(targ,pred), dtype='float32') #cast bool tensor to float

  # 0 is padding, don't include those- mask is tensor representing non-pad value
  mask = K.cast(K.greater(targ, 0), dtype='float32') #cast bool-tensor to float 
  n_correct = K.sum(mask * correct) #
  n_total = K.sum(mask)
  return n_correct / n_total

#custom loss because we dont want to consider padding
def loss(y_true, y_pred):
   # both are of shape ( _, Ty, VOCAB_SIZE )
  mask = K.cast(y_true > 0, dtype='float32')
  out = mask * y_true * K.log(y_pred) #cross entopy loss
  return -K.sum(out) / K.sum(mask)

models = Model( VOCAB_SIZE, MAX_LEN, embedding_matrix )
train_model = models.model_train_teacher_forcing()
train_model.compile( optimizer="adam", loss=loss, metrics=[acc])

print("Training Started")
all_metrics = []
BATCH_SIZE = 224
TRAIN_BATCHES, VAL_BATCHES = len(x_train)//BATCH_SIZE, len(x_val)//BATCH_SIZE
for epoch in range(len(all_metrics)+1, 15):
  tloss, tacc, ti, t0 = 0,0,0,time.time()
  for x,y in batch_generator( x_train, y_train, ytf_train, batch_size=BATCH_SIZE):
    metrics_train = train_model.train_on_batch(x, y)
    tloss, tacc, ti = tloss+metrics_train[0], tacc+metrics_train[1], ti+1
    print(f'\rTraining Progress: {ti}/{TRAIN_BATCHES} - loss: {tloss/ti:.4f} - acc: {tacc/ti:.4f}', end="")

  vloss, vacc, vi = 0, 0, 0
  for x,y in batch_generator( x_val, y_val, ytf_val, batch_size=BATCH_SIZE ):
    metrics_val = train_model.test_on_batch(x, y)
    vloss, vacc, vi = vloss+metrics_val[0], vacc+metrics_val[1], vi+1
    print(f'\rValidation Progress: {vi}/{VAL_BATCHES} - val_loss: {vloss/vi:.4f} - val_acc: {vacc/vi:.4f}', end="")

  all_metrics.append( ( tloss/ti, tacc/ti, vloss/vi, vacc/vi  ) )
  print(f"\rEpoch {epoch:2.0f} - {(time.time()-t0):.0f}s - loss: {tloss/ti:.4f} - acc: {tacc/ti:.4f} - val_loss: {vloss/vi:.4f} - val_acc: {vacc/vi:.4f}")

caption_generator = models.model_predict_caption()
tf.saved_model.save(caption_generator, 'caption_generator/1')
print("Model Saved")