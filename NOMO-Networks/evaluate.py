from __future__ import print_function

import os
import sys
import tensorflow as tf 
import imageio
import numpy as np 
from scipy.io import loadmat, savemat
from argparse import ArgumentParser
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

parser = ArgumentParser()
parser.add_argument("--model_definitions", default='ModelDefinitions_AlexNet')
parser.add_argument("--model_path",   default='')
parser.add_argument("--front_path",   default='')
parser.add_argument("--side_path",    default='')
parser.add_argument("--output_path",  default='')
parser.add_argument("--sampleList",   default='')
parser.add_argument("--dump_path",    default='')
parser.add_argument("--img_format",   default='.png')
parser.add_argument("--use_gpu",      default=1,   type=int)
parser.add_argument("--img_channels", default=1,   type=int)
parser.add_argument("--img_rows",     default=224, type=int)
parser.add_argument("--img_cols",     default=124, type=int)

FLAGS = parser.parse_args()

MODEL_PATH  = FLAGS.model_path
FRONT_PATH  = FLAGS.front_path
SIDE_PATH   = FLAGS.side_path
OUTPUT_PATH = FLAGS.output_path
DUMP_PATH   = FLAGS.dump_path
SAMPLELIST  = FLAGS.sampleList
USE_GPU     = FLAGS.use_gpu
IMG_FORMAT  = FLAGS.img_format
IMG_ROWS    = FLAGS.img_rows
IMG_COLS    = FLAGS.img_cols
IMG_CHANNELS = FLAGS.img_channels
MODEL_DEFINATIONS = FLAGS.model_definitions

if not os.path.exists(DUMP_PATH): os.mkdir(DUMP_PATH)
LOG_FOUT = open(os.path.join(DUMP_PATH, 'log_evaluate.txt'), 'w')

def log_string(out_str):
	LOG_FOUT.write(out_str+'\n')
	LOG_FOUT.flush()
#----------------------------------------------------------------------------------------------------
def print_args(args):
	log_string("------ Testing Parameters ------------")
	log_string("--model_path   : %s" %args.model_path)
	log_string("--front_path   : %s" %args.front_path)
	log_string("--side_path    : %s" %args.side_path)
	log_string("--output_path  : %s" %args.output_path)
	log_string("--sampleList   : %s" %args.sampleList)
	log_string("--use_gpu      : %d" %args.use_gpu)
	log_string("--img_format   : %s" %args.img_format)
	log_string("--img_channels : %d" %args.img_channels)
	log_string("--img_rows     : %d" %args.img_rows)
	log_string("--img_cols     : %d" %args.img_cols)
	log_string("--model_definitions : %s" %args.model_definitions)
	log_string("---------------------------------------")

def load_image(fname, img_channels=3):
	img = imageio.imread(fname)  # H*W*C
	if img_channels==1:
		img = np.expand_dims(img, -1) # H*W*1
	return img
#----------------------------------------------------------------------------------------------------
def evaluate():

	print_args(FLAGS)

	if MODEL_PATH:
		# load samplelist
		if SAMPLELIST:
			sampleNames = loadmat(SAMPLELIST)['sampleNames']
			sampleNames = [x[0][0]+IMG_FORMAT for x in sampleNames]
		else:
			sampleNames = os.listdir(FRONT_PATH)
		log_string("Totall %d samples"%len(sampleNames))

		if not os.path.exists(OUTPUT_PATH): os.mkdir(OUTPUT_PATH)

		device = '/gpu:0' if USE_GPU else '/cpu:0'
		log_string('Device: %s'%device)

		with tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=False)) as sess:
			saver = tf.compat.v1.train.import_meta_graph(MODEL_PATH+'UF-US-2-network.ckpt.meta', clear_devices=True)
			saver.restore(sess, MODEL_PATH+'UF-US-2-network.ckpt')

			with tf.device(device):
				graph = tf.get_default_graph()
				X_f  = graph.get_tensor_by_name("X_front:0")
				X_s  = graph.get_tensor_by_name("X_side:0")
				drop = graph.get_tensor_by_name("drop_rate:0")
				if MODEL_DEFINATIONS == 'ModelDefinitions_HKS':
					pred = graph.get_tensor_by_name("fc_layers/fc6/BiasAdd:0") # old HKS-Net network
				else:
					pred = graph.get_tensor_by_name("fc_layers/fc3_squeezed:0")
					
				for sampleName in sampleNames:
					# change to Channels-last
					test_x_f = np.zeros((1, IMG_ROWS, IMG_COLS, IMG_CHANNELS), dtype=float)
					test_x_f[0, :, :, :] = load_image(FRONT_PATH+sampleName, img_channels=IMG_CHANNELS)
					test_x_s = np.zeros((1, IMG_ROWS, IMG_COLS, IMG_CHANNELS), dtype=float)
					test_x_s[0, :, :, :] = load_image(SIDE_PATH+sampleName, img_channels=IMG_CHANNELS)

					feed_dict = {X_f: test_x_f, X_s: test_x_s, drop: 0}
					test_pred = sess.run(pred, feed_dict)
					test_pred = test_pred[0, :]
					savemat(OUTPUT_PATH+sampleName[:-4]+'.mat', {'pred':test_pred})

		log_string("Testing Done")
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	#
	evaluate()

	LOG_FOUT.close()
