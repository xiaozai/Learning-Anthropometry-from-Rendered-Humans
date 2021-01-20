from __future__ import print_function

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf 
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR) 
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
				   filters=64,
				   kernel_size=(11,11),
				   padding='valid',
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
				   filters=192,
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
				   filters=384,
				   kernel_size=(3,3),
				   padding='same',
				   kernel_initializer=tf.contrib.layers.xavier_initializer(),
				   data_format='channels_last',
				   reuse=reuseFlag,
				   name='conv3')
	relu3 = ReLU(name='relu3')(conv3)

	conv4 = conv2d(inputs=relu3,
				   filters=384,
				   kernel_size=(3,3),
				   padding='same',
				   kernel_initializer=tf.contrib.layers.xavier_initializer(),
				   data_format='channels_last',
				   reuse=reuseFlag,
				   name='conv4')
	relu4 = ReLU(name='relu4')(conv4)

	conv5 = conv2d(inputs=relu4,
				   filters=256,
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
	
	return pool3

# Use conv2d instead of fully_connected layers.
def FullyBlock(X, num_classes, drop_rate=0.5, scopName='fc_layers'):
	with tf.variable_scope(scopName):

		net = conv2d(inputs=X, filters=4096, kernel_size=(5,5), padding='valid', name='fc1')
		net = Dropout(rate=drop_rate, name='dropout1')(net)
		net = conv2d(inputs=net, filters=4096, kernel_size=(1,1), name='fc2')
		net = Dropout(rate=drop_rate, name='dropout1')(net)
		net = tf.reduce_mean(net, [1,2], keep_dims=True, name='global_pool')
		net = conv2d(inputs=net, filters=num_classes, kernel_size=(1,1), name='fc3')
		net = tf.squeeze(net, [1, 2], name='fc3_squeezed')
	return net

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
	# loss = tf.losses.mean_squared_error(labels, prediction)      # L2 / MSE loss
	# loss = tf.reduce_sum(tf.abs(labels - prediction))            # L1 loss

	weights = tf.constant([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 50, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
	loss = tf.math.reduce_mean(tf.math.multiply(tf.math.reduce_mean(tf.math.square(labels - prediction), axis=0), weights))

	return loss

def get_thresholdLoss(labels, prediction):
	thresholds = tf.constant([3.2, 1.9, 4.2, 5.6, 7.1, 6.9, 1.6, 2.6, 2.2, 2.3, 4.3, 5.1, 2.7, 1.4, 7.1, 2.1])
	loss = tf.nn.l2_loss(tf.math.abs(labels - prediction) - thresholds)
	return loss

if __name__ == '__main__':
	with tf.Graph().as_default():
		inputs_f = tf.zeros((32, 224,224,1))
		inputs_s = tf.zeros((32, 224,224,1))
		Y = tf.zeros((32, 16))
		outputs = get_model(inputs_f, inputs_s, 16)
		print(outputs)
		loss = get_weightedLoss(Y, outputs)
		print(loss)