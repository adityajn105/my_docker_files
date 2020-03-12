from tensorflow.keras import models, layers
def build(weights):
	inp = layers.Input( shape=(28,28,1) )
	c1 = layers.Conv2D( 64, (5,5), padding="same", activation="relu", kernel_initializer="he_normal" )(inp)
	p1 = layers.MaxPooling2D( pool_size=(2,2) )(c1)
	c2 = layers.Conv2D( 64, (3,3), padding="same", activation="relu", kernel_initializer="he_normal")(p1)
	p2 = layers.MaxPooling2D(pool_size=(2,2))(c2)
	c3 = layers.Conv2D( 32, (2,2), padding="same", activation="relu", kernel_initializer="he_normal" )(c2)
	p3 = layers.MaxPooling2D(pool_size=(2,2))(c3)
	f1 = layers.Flatten()(p3)
	d1 = layers.Dense(256, activation="relu")(f1)
	d1 = layers.Dropout(0.4)(d1)
	d2 = layers.Dense(64, activation="relu")(d1)
	d2 = layers.Dropout(0.2)(d2)
	out = layers.Dense(10, activation="softmax")(d2)
	model = models.Model( inp, out  )
	model.load_weights(weights)
	return model