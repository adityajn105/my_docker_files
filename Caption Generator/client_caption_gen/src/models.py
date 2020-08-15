from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.layers import GlobalAveragePooling2D

from tensorflow.keras.layers import LSTM, Dense, Lambda, Concatenate, Input, Embedding
from tensorflow.keras import backend as K

from tensorflow.keras.models import Model

class Model():

	def __init__(self, VOCAB_SIZE, MAX_LEN, embedding_matrix):
		self.MAX_LEN = MAX_LEN
		self.vgg19 = VGG19( include_top=False, weights="imagenet", input_shape=(224,224,3) )
		for layer in self.vgg19.layers:
  			layer.trainable=False
  		self.img_feature = GlobalAveragePooling2D()( self.vgg19.layers[-1].output )

  		self.initial_h = Input( shape=( 512, ) )
		self.initial_c = Input( shape=( 512, ) )

		self.embedding_layer = Embedding( VOCAB_SIZE, 50, weights=[embedding_matrix], trainable=False )
		self.lstm = LSTM( 512, return_state=True, name="decoder_lstm", recurrent_dropout=0.1 )

		self.concat = Concatenate(axis=-1)
		self.dense = Dense(1024, activation='relu')
		self.next_word = Dense(VOCAB_SIZE, activation='softmax')

		# to change outputs shape to (_, MAX_LENGTH, VOCAB_SIZE)
		def stack_and_transpose(x):
			  x = K.stack(x) # it will convert list to a tensor of ( MAX_LENGTH, _, VOCAB_SIZE )
			  x = K.permute_dimensions( x, pattern=(1,0,2) ) #(_, MAX_LENGTH, VOCAB_SIZE)
			  return x

		self.stacker = Lambda(stack_and_transpose, name="stack_and_transpose")


	def model_train_teacher_forcing(self):
		lstm_input = Input( shape=(MAX_LEN) ) #for teacher forcing
		embeddings = self.embedding_layer(lstm_input) 

		hidden_state = self.initial_h
		cell_state = self.initial_c

		outputs = []
		for t in range(self.MAX_LEN):
		  selector = Lambda( lambda x: x[:,t:t+1], name=f"selector_{t}" ) #for teacher forcing
		  word_embedding = selector(embeddings) #embedding of next word

		  _, hidden_state, cell_state = self.lstm( word_embedding, initial_state=[hidden_state,cell_state] )

		  combined = self.concat([img_feature, hidden_state])
		  final_feature = self.dense(combined)

		  output = self.next_word( final_feature )
		  outputs.append(output)

		outputs = self.stacker(outputs) #(_, MAX_LENGTH, VOCAB_SIZE)

		return Model( [ self.vgg19.input, lstm_input, self.initial_h, self.initial_c ], outputs)

	def model_predict_caption(self):
		token = Input( shape=(1,) ) #( _,1 ) #init_token - <sos>
		word_embedding = self.embedding_layer(token)
		hidden_state, cell_state = self.initial_h, self.initial_c

		token_new = token
		next_token = Lambda( lambda x: K.expand_dims(K.argmax(x,axis=-1), axis=-1), name="next_token")
		outputs = []
		for _ in range(self.MAX_LEN):
		  _, hidden_state, cell_state = self.lstm( word_embedding, initial_state=[hidden_state,cell_state] )

		  combined = self.concat([img_feature, hidden_state])
		  final_feature = self.dense(combined)
		  
		  output = self.next_word( final_feature )

		  token_new = next_token( output )
		  word_embedding = self.embedding_layer(token_new) 

		  outputs.append(output) 

		outputs = self.stacker(outputs)
		return Model( [ self.vgg19.input, token, self.initial_h, self.initial_c ], outputs )
	_
	