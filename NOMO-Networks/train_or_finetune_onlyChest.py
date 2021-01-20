from __future__ import print_function

import tensorflow as tf 
import importlib

import os
import sys
import numpy as np 
import InputGenerators as ig
from argparse import ArgumentParser
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

parser = ArgumentParser()
parser.add_argument("--learning_rate",   default=1e-4, type=float, help='learning rate')
parser.add_argument("--lr_decay_step",   default=0,    type=int,   help='after each epoch, lr decreases')
parser.add_argument("--lr_decay_rate",   default=0.1,  type=float, help='new lr = lr * rate')
parser.add_argument("--batch_size",      default=32,   type=int,   help='batch size')
parser.add_argument("--nb_epoch",        default=30,   type=int,   help="num of trianing epochs")
parser.add_argument('--input_channels',  default=1,    type=int,   help='1 for silh, 3 for RGB')
parser.add_argument('--input_rows',      default=224,  type=int,   help="Image Height")
parser.add_argument('--input_cols',      default=124,  type=int,   help="Image Width")
parser.add_argument("--num_classes",     default=26,   type=int,   help="dimension of the labels")
parser.add_argument("--share_weights",   default=0,    type=int,   help="0 no share; 1 share weights")
parser.add_argument("--model_definitions",default='ModelDefinitions_HKS')
parser.add_argument("--pre_model_path",  default='')
parser.add_argument('--output_path',     default='')
parser.add_argument("--train_files",     default='')
parser.add_argument("--test_files",      default='')

FLAGS = parser.parse_args()

LEARNING_RATE  = FLAGS.learning_rate
LR_DECAY_STEP  = FLAGS.lr_decay_step
LR_DECAY_RATE  = FLAGS.lr_decay_rate
BATCH_SIZE     = FLAGS.batch_size
NB_EPOCH       = FLAGS.nb_epoch
INPUT_CHANNELS = FLAGS.input_channels
INPUT_ROWS     = FLAGS.input_rows
INPUT_COLS     = FLAGS.input_cols
NUM_CLASSES    = FLAGS.num_classes
SHARE_WEIGHTS  = FLAGS.share_weights
PRE_MODEL_PATH = FLAGS.pre_model_path
OUTPUT_PATH    = FLAGS.output_path
TRAIN_FILES    = ig.getDataFiles(FLAGS.train_files)
TEST_FILES     = ig.getDataFiles(FLAGS.test_files)

# import network module
MODEL_DEFINITIONS = FLAGS.model_definitions 
MODEL = importlib.import_module(MODEL_DEFINITIONS)
#
LOG_PATH = os.path.join(OUTPUT_PATH, 'logs')
if not os.path.exists(LOG_PATH): os.mkdir(LOG_PATH)
LOG_FOUT = open(os.path.join(LOG_PATH, 'log_train.txt'), 'w')

GRAPH_PATH = os.path.join(OUTPUT_PATH, 'graph')
if not os.path.exists(GRAPH_PATH): os.mkdir(GRAPH_PATH)

MODEL_PATH = os.path.join(OUTPUT_PATH, 'model')
if not os.path.exists(MODEL_PATH): os.mkdir(MODEL_PATH)

def log_string(out_str):
	LOG_FOUT.write(out_str+'\n')
	LOG_FOUT.flush()
#----------------------------------------------------------------------------------------------------
def print_args(args):
	log_string("------ Training Parameters ------------")
	log_string("--learning_rate   : %f" %args.learning_rate)
	log_string("--lr_decay_step   : %d" %args.lr_decay_step)
	log_string("--lr_decay_rate   : %f" %args.lr_decay_rate)
	log_string("--batch_size      : %d" %args.batch_size)
	log_string("--nb_epoch        : %d" %args.nb_epoch)
	log_string("--input_rows      : %d" %args.input_rows)
	log_string("--input_cols      : %d" %args.input_cols)
	log_string("--input_channels  : %d" %args.input_channels)
	log_string("--num_classes     : %d" %args.num_classes)
	log_string("--pre_model_path  : %s" %args.pre_model_path)
	log_string("--output_path     : %s" %args.output_path)
	log_string("--train_files     : %s" %args.train_files)
	log_string("--test_files      : %s" %args.test_files)

	log_string("---------------------------------------")
	sys.stdout.flush()
#----------------------------------------------------------------------------------------------------
def train_or_finetune():

	device = '/gpu:0'

	with tf.Graph().as_default():
		with tf.device(device):
			# Placeholders
			X_f, X_s, Y, LR, drop = MODEL.placeholder_inputs(INPUT_ROWS, INPUT_COLS, INPUT_CHANNELS, NUM_CLASSES)
			# Construct Network Graph, (batchsize, H, W, Channels)
			pred_op = MODEL.get_model(X_f, X_s, NUM_CLASSES, reuseFlag=bool(SHARE_WEIGHTS), drop_rate=drop)
			loss_op = MODEL.get_loss(Y, pred_op)
			#
			tf.summary.scalar('learning_rate', LR)
			tf.summary.scalar('loss', loss_op)
			# Note the global_step=batch parameter to minimize.
			# That tells the optimizer to helpfully increment the 'batch' parameter 
			# for you every time it trains.
			step = tf.Variable(0) # 
			optimizer = tf.train.AdadeltaOptimizer(learning_rate=LR, name='adadelta')
			train_op  = optimizer.minimize(loss_op, global_step=step)   

		# create a session
		config = tf.compat.v1.ConfigProto()
		config.gpu_options.allow_growth = True
		config.allow_soft_placement = True
		config.log_device_placement = True
		with tf.compat.v1.Session(config=config) as sess:
			# Add summary writers
			merged = tf.summary.merge_all()
			train_writer = tf.summary.FileWriter(GRAPH_PATH, sess.graph)
			train_saver  = tf.train.Saver()

			if PRE_MODEL_PATH:
				log_string('-- load pretrained model from %s'%PRE_MODEL_PATH)
				train_saver.restore(sess, os.path.join(PRE_MODEL_PATH, 'UF-US-2-network.ckpt'))
			else:
				sess.run(tf.global_variables_initializer()) # Init variables

			ops = {'X_f': X_f, 'X_s' : X_s,  'Y': Y,
				   'LR' : LR,  'drop': drop, 'step': step, 'merged' : merged, 
				   'pred_op': pred_op, 'loss_op': loss_op, 'train_op': train_op,
				   'TRAIN_FILES': TRAIN_FILES, 'TEST_FILES': TEST_FILES, 'BATCH_SIZE': BATCH_SIZE}

			best_loss = 1e20
			for epoch in range(NB_EPOCH):
				log_string('------ EPOCH %03d ------'%epoch)
				# update the learning rate every epoch
				if LR_DECAY_STEP:
					lr_value = LEARNING_RATE * (LR_DECAY_RATE**(epoch//LR_DECAY_STEP))
				else:
					lr_value = LEARNING_RATE
				log_string('--lr = %f ------'%lr_value)

				train_one_epoch(sess, ops, lr_value, train_writer)
				epoch_loss = evaluate_one_epoch(sess, ops)

				if epoch_loss < best_loss:
					best_loss = epoch_loss
					save_path = train_saver.save(sess, os.path.join(MODEL_PATH, 'UF-US-2-network.ckpt'))
					log_string("Best Epoch : %d, Best Model saved in file: %s"%(epoch, save_path))
		
def train_one_epoch(sess, ops, learning_rate, train_writer):
	# Shuffle train files
	TRAIN_FILES, BATCH_SIZE = ops['TRAIN_FILES'], ops['BATCH_SIZE']
	train_file_idxs = np.arange(0, len(TRAIN_FILES))
	np.random.shuffle(train_file_idxs)

	loss_epoch = 0

	for fn in range(len(train_file_idxs)):

		data_front, data_side, label = ig.loadDataFile_onlyChest(TRAIN_FILES[train_file_idxs[fn]], shuffleFlag=True)

		file_size = data_front.shape[0]
		num_batches = file_size//BATCH_SIZE

		loss_sum = 0

		for batch_idx in range(num_batches):
			start_idx = batch_idx * BATCH_SIZE
			end_idx   = (batch_idx + 1) * BATCH_SIZE

			feed_dict = {ops['X_f']: data_front[start_idx:end_idx, ...],
						 ops['X_s']: data_side[start_idx:end_idx, ...],
						 ops['Y']  : label[start_idx:end_idx, ...],
						 ops['LR'] : learning_rate, 
						 ops['drop']: 0.5}
			summary, loss_val, pred_val, _, istep = sess.run([ops['merged'], 
															  ops['loss_op'], 
															  ops['pred_op'], 
															  ops['train_op'], 
															  ops['step']],
															 feed_dict=feed_dict) 
			train_writer.add_summary(summary, istep)
			loss_sum += loss_val
		# log_string('--train file Idx: %d, mean loss : %f'%(fn, loss_sum / float(num_batches)))
		loss_epoch += loss_sum / float(num_batches)
	log_string('--train loss : %f'%(loss_epoch / float(len(train_file_idxs))))

def evaluate_one_epoch(sess, ops):
	TEST_FILES, BATCH_SIZE = ops['TEST_FILES'], ops['BATCH_SIZE']
	test_files_idx = np.arange(0, len(TEST_FILES))

	loss_evaluate = 0
	for fn in range(len(test_files_idx)):
		data_front, data_side, label = ig.loadDataFile_onlyChest(TEST_FILES[test_files_idx[fn]], shuffleFlag=False)
		file_size = data_front.shape[0]
		num_batches = file_size // BATCH_SIZE

		loss_sum = 0
		for batch_idx in range(num_batches):
			start_idx = batch_idx * BATCH_SIZE
			end_idx   = (batch_idx + 1) * BATCH_SIZE

			feed_dict = {ops['X_f']: data_front[start_idx:end_idx, ...],
						 ops['X_s']: data_side[start_idx:end_idx, ...],
						 ops['Y']  : label[start_idx:end_idx, ...],
						 ops['drop']: 0}
			loss_val = sess.run(ops['loss_op'], feed_dict=feed_dict)
			loss_sum += loss_val
		# log_string('--- test file Idx: %d, mean loss : %f'%(fn, loss_sum / float(num_batches)))
		loss_evaluate += loss_sum / float(num_batches)
	log_string('--test loss : %f'%(loss_evaluate / float(len(test_files_idx))))
	return loss_evaluate / float(len(test_files_idx))
#----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

	print_args(FLAGS)

	train_or_finetune()
	
	LOG_FOUT.close()