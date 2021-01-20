import tensorflow as tf
print(tf.__version__)

from tensorflow.contrib import predictor

import ModelDefinitions_HKS as md
import imageio
import os
import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--model_path",   default='./exp/female_224x224Silh_27D_group10_hks/model/')
parser.add_argument('--output_path',  default='./exp/female_224x224Silh_27D_group10_hks/saved_model/')
parser.add_argument("--test_path",    default='./exp/female_224x224Silh_27D_group10_hks/testIMG/')
parser.add_argument('--img_rows',     type=int, default=224)
parser.add_argument('--img_cols',     type=int, default=224)
parser.add_argument('--img_channels', type=int, default=1)
parser.add_argument('--num_classes',  type=int, default=27)
FLAGS = parser.parse_args()

IMG_C = FLAGS.img_channels
IMG_H = FLAGS.img_rows
IMG_W = FLAGS.img_cols
NUM_CLASSES = FLAGS.num_classes
MODEL_PATH  = FLAGS.model_path
OUTPUT_PATH = FLAGS.output_path
TEST_PATH   = FLAGS.test_path

def loadImg(fname):
	I = imageio.imread(fname) # H*W 
	if len(I.shape) < 3: # H*W
		I = np.expand_dims(I, -1) # H*W*1
		I = np.expand_dims(I, 0)  # 1*H*W*1
	return I

def saveModel():
	with tf.Graph().as_default():
		# Construct Network Graph
		X_f  = tf.placeholder(tf.float32, [None, IMG_H, IMG_W, IMG_C], name='X_front')
		X_s  = tf.placeholder(tf.float32, [None, IMG_H, IMG_W, IMG_C], name='X_side')
		pred = md.get_model(X_f, X_s, num_classes=NUM_CLASSES, reuseFlag=False, drop_rate=0)
		# Add ops to save and restore all the variables
		saver = tf.train.Saver()
		with tf.Session() as sess:
			# Restore variables from disk
			saver.restore(sess,  MODEL_PATH+'UF-US-2-network.ckpt')
			# The easiest way to create a SavedModel
			tf.saved_model.simple_save(sess, 
									   OUTPUT_PATH,
									   inputs={'X_f': X_f, 'X_s': X_s},
									   outputs={'pred': pred})

def loadModel():
	# Load testing images
	I_front = loadImg(os.path.join(TEST_PATH, 'front.png')) # 1*H*W*1
	I_side  = loadImg(os.path.join(TEST_PATH, 'side.png'))  # 1*H*W*1
	# Prediction with saved_model
	predict_fn = predictor.from_saved_model(OUTPUT_PATH)
	predictions = predict_fn({"X_f":I_front, "X_s":I_side})
	print(predictions)

if __name__ == '__main__':

	# saveModel()

	loadModel()