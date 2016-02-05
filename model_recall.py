import numpy as np
import h5py
import cPickle
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout, Flatten
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.utils import np_utils
from keras import callbacks
from keras.utils.visualize_util import plot
from keras.layers import advanced_activations

obs_size = 64
# used the cnn_copy.py script to establish this (1.298046...)
# rounded up to 1.3 for safety
max_train = 1.3

print('Reading data')

## Initialising with value 0
f = h5py.File('keras_data/output/db_Oregon_X_0.hdf5', 'r')
X = np.array(f['data'])
f.close()
#f = h5py.File('keras_data/db_Oregon_y_0.hdf5', 'r')
#y_train = np.array(f['data'])
#f.close()

for i in range(1,10):
	f = h5py.File('keras_data/output/db_Oregon_X_%d.hdf5' % i, 'r')
	X = np.vstack((X, np.array(f['data'])))
	f.close()
	#f = h5py.File('keras_data/db_Oregon_y_%d.hdf5' % i, 'r')
	#y_train = np.hstack((y_train, f['data']))
	#f.close()

## Initialising with value 0
#f = h5py.File('keras_data/db_Washington_X_0.hdf5', 'r')
#X_test = np.array(f['data'])
#f.close()
#f = h5py.File('keras_data/db_Washington_y_0.hdf5', 'r')
#y_test = np.array(f['data'])
#f.close()

#for i in range(1,26):
#	f = h5py.File('keras_data/db_Washington_X_%d.hdf5' % i, 'r')
#	X_test = np.vstack((X_test, np.array(f['data'])))
#	f.close()
#	f = h5py.File('keras_data/db_Washington_y_%d.hdf5' % i, 'r')
#	y_test = np.hstack((y_test, f['data']))
#	f.close()

print X.shape

# mean normalisation
mean_value = np.mean(X)
X = X - mean_value
std_value = np.std(X)
X = X / std_value

def create_model():
	model = Sequential()
	# first convolutional pair
	model.add(Convolution2D(32, 5, 5, 
            border_mode='valid',
            input_shape = (7, obs_size, obs_size)))
	model.add(Activation('relu'))
	model.add(Convolution2D(32, 5, 5))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	# second convolutional pair
	model.add(Convolution2D(64, 3, 3, border_mode='valid'))
	model.add(Activation('relu'))
	model.add(Convolution2D(64, 3, 3))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	# third convolutional pair
	model.add(Convolution2D(128, 3, 3, border_mode='valid'))
	model.add(Activation('relu'))
	model.add(Convolution2D(128, 3, 3))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.25))
	# convert convolutional filters to flat so they
	# can be fed to fully connected layers
	model.add(Flatten())
	# first fully connected layer
	model.add(Dense(512))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	# classification fully connected layer
	model.add(Dense(1))
	model.add(Activation('linear'))
	#
	return model


# setting sgd optimizer parameters
#sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)

model_loaded = create_model()
model_loaded.compile(loss='mean_squared_error', optimizer='rmsprop')
model_loaded.load_weights('model_weights.h5')

y_pred = model_loaded.predict(X)

def un_normalise_y(y_pred, max_train):
	"""
	Takes the normalised y and unnormalises import
	"""
	## times by max_train
	y_pred *= max_train
	## raise to power of ten
	y_pred = (y_pred+1)**10 - 1
	return y_pred


y_pred = un_normalise_y(y_pred, max_train)

f = file('output_predictions.save', 'wb')
cPickle.dump(y_pred, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()





