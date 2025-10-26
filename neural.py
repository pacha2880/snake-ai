import snake
from snake import game
# import snakeTrain
# from snakeTrain import game

import tensorflow as tf
from tensorflow import keras
import numpy as np

# model = keras.Sequential()
# model.add(keras.layers.Dense(5, activation='relu', input_dim=5))
# model.add(keras.layers.Dense(25, activation='relu'))
# model.add(keras.layers.Dense(1, activation='sigmoid'))
# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model = keras.models.load_model("models/model2000.h5")
g = game()
while True:
	state = g.getState()

	train_labels = [0,0,0]

	if state[3] > 1e-9 and state[0] == 0:
		train_labels[0] = 1
	elif state[3] < -1e-9 and state[2] == 0:
		train_labels[2] = 1
	elif state[1] == 0:
		train_labels[1] = 1
	elif state[0] == 0:
		train_labels[0] = 1
	elif state[2] == 0:
		train_labels[2] = 1

	train_input = np.array([[state[0], state[1], state[2], state[3], -1], [state[0], state[1], state[2], state[3], 0], [state[0], state[1], state[2], state[3], 1]])
	train_labels = np.array(train_labels)

	predictions = model.predict(train_input)
	ind = np.argmax([predictions[0][0], predictions[1][0], predictions[2][0]])

	if ind == 0:
		g.next([1,0,0])
	elif ind == 1:
		g.next([0,1,0])
	else:
		g.next([0,0,1])

	# print(train_input)
	# print(train_labels)
	# model.fit(train_input, train_labels, epochs = 1, verbose = 0)
	

# model.save("models/model30it.h5")

