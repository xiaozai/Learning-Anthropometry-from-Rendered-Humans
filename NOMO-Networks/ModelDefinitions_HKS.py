from __future__ import print_function

import tensorflow as tf 
from tensorflow.keras.layers import MaxPool2D, Dense
from tensorflow.keras.layers import Flatten, ReLU, Dropout

from tensorflow.layers import conv2d

def placeholder_inputs(img_rows, img_cols, img_channels, num_classes):
	X_f = tf.placeholder(tf.float32, [None, img_rows, img_cols, img_channels], name='X_front')
	X_s = tf.placeholder(tf.float32, [None, img_rows, img_cols, img_channels], name='X_side')
	Y   = tf.placeholder(tf.float32, [None, num_classes], name='Y')
	LR  = tf.placeholder(tf.float32, shape=(), name='lr')
	drop= tf.placeholder(tf.float32, shape=(), name='drop_rate')
	return X_f, X_s, Y, LR, drop

def ConvBlock(X, reuseFlag=None):
	# (batch, height, width, channels)
	conv1 = conv2d(inputs=X,
				   filters=48,
				   kernel_size=(11,11),
				   padding='same',
				   kernel_initializer=tf.contrib.layers.xavier_initializer(),
				   data_format='channels_last',
				   reuse=reuseFlag,
				   name='conv1')
	relu1 = ReLU(name='relu1')(conv1)
	pool1 = MaxPool2D(pool_size=(3,3),
					  padding='valid',
					  data_format='channels_last',
					  name='pool1')(relu1)

	conv2 = conv2d(inputs=pool1, 
				   filters=128,
				   kernel_size=(5,5),
				   padding='same',
				   kernel_initializer=tf.contrib.layers.xavier_initializer(),
				   data_format='channels_last',
				   reuse=reuseFlag,
				   name='conv2')
	relu2 = ReLU(name='relu2')(conv2)
	pool2 = MaxPool2D(pool_size=(3,3),
					  padding='valid',
					  data_format='channels_last',
					  name='pool2')(relu2)

	conv3 = conv2d(inputs=pool2,
				   filters=192,
				   kernel_size=(3,3),
				   padding='same',
				   kernel_initializer=tf.contrib.layers.xavier_initializer(),
				   data_format='channels_last',
				   reuse=reuseFlag,
				   name='conv3')
	relu3 = ReLU(name='relu3')(conv3)

	conv4 = conv2d(inputs=relu3,
				   filters=192,
				   kernel_size=(3,3),
				   padding='same',
				   kernel_initializer=tf.contrib.layers.xavier_initializer(),
				   data_format='channels_last',
				   reuse=reuseFlag,
				   name='conv4')
	relu4 = ReLU(name='relu4')(conv4)

	conv5 = conv2d(inputs=relu4,
				   filters=128,
				   kernel_size=(3,3),
				   padding='same',
				   kernel_initializer=tf.contrib.layers.xavier_initializer(),
				   data_format='channels_last',
				   reuse=reuseFlag,
				   name='conv5')
	relu5 = ReLU(name='relu5')(conv5)
	pool3 = MaxPool2D(pool_size=(3,3),
					  padding='valid',
					  data_format='channels_last',
					  name='pool3')(relu5)
	out = Flatten(data_format='channels_last', name='Flatten')(pool3)

	return out

def FullyBlock(X, num_classes, drop_rate=0.5, scopName='fc_layers'):
	with tf.variable_scope(scopName):
		fc1   = Dense(4096, name='fc1')(X)
		drop1 = Dropout(rate=drop_rate, name='dropout1')(fc1)
		relu6 = ReLU(name='relu6')(drop1)

		fc2   = Dense(2048, name='fc2')(relu6)
		relu7 = ReLU(name='relu7')(fc2)

		fc3   = Dense(4224, name='fc3')(relu7)

		fc4   = Dense(4096, name='fc4')(fc3)
		drop2 = Dropout(rate=drop_rate, name='dropout2')(fc4)
		relu8 = ReLU(name='relu8')(drop2)

		fc5   = Dense(2048, name='fc5')(relu8)
		relu9 = ReLU(name='relu9')(fc5)

		fc6   = Dense(num_classes, name='fc6')(relu9)

	return fc6

def get_model(x_f, x_s, num_classes, reuseFlag=False, drop_rate=0.5):

	if reuseFlag:
		with tf.variable_scope('convs', reuse=None):
			out_f = ConvBlock(x_f, reuseFlag=None)
		with tf.variable_scope('convs', reuse=True):
			out_s = ConvBlock(x_s, reuseFlag=True)
	else:
		with tf.variable_scope('convs_f', reuse=False):
			out_f = ConvBlock(x_f, reuseFlag=False)
		with tf.variable_scope('convs_s', reuse=False):
			out_s = ConvBlock(x_s, reuseFlag=False)

	out  = tf.maximum(out_f, out_s) # merge
	pred = FullyBlock(out, num_classes, drop_rate=drop_rate)

	return pred

def get_loss(labels, prediction):
	loss = tf.losses.mean_squared_error(labels, prediction)
	return loss