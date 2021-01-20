from __future__ import print_function

import numpy as np 
import random
from scipy.io import loadmat, savemat

import tensorflow as tf 

import InputGenerators_CAESAR as ig 
import ModelDefinitions as md 

import os
import sys
#---------------------------------------------------------------------------------------
def test_UF_US_2(pretrained_model = '',
				 front_dir        = '',
				 side_dir         = '',
				 output_dir       = '',
				 sampleList       = '',
				 img_format       = '.png',
				 use_gpu          = 0,
				 img_channels     = 3,
				 img_rows         = 480,
				 img_cols         = 200):

	if pretrained_model:

		if sampleList:
			sampleNames = loadmat(sampleList)['sampleNames']
			sampleNames = [x[0][0]+img_format for x in sampleNames]
		else:
			sampleNames = os.listdir(front_dir)
		print("Totall %d samples"%len(sampleNames))

		if not os.path.exists(output_dir): os.mkdir(output_dir)

		device = '/gpu:0' if use_gpu else '/cpu:0'
		print('Device: %s'%device)

		with tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True)) as sess:
			saver = tf.compat.v1.train.import_meta_graph(pretrained_model+'UF-US-2-network.ckpt.meta', clear_devices=True)
			saver.restore(sess, pretrained_model+'UF-US-2-network.ckpt')

			with tf.device(device):
				graph = tf.get_default_graph()

				X_f  = graph.get_tensor_by_name("X_front:0")
				X_s  = graph.get_tensor_by_name("X_side:0")
				drop = graph.get_tensor_by_name("drop_rate:0")
				pred = graph.get_tensor_by_name("fc_layers/fc6/BiasAdd:0")

				for sampleName in sampleNames:
					# change to Channels-last
					test_x_f = np.zeros((1, img_rows, img_cols, img_channels), dtype=float)
					test_x_f[0, :, :, :] = ig.load_image(front_dir+sampleName, img_channels=img_channels)
					test_x_s = np.zeros((1, img_rows, img_cols, img_channels), dtype=float)
					test_x_s[0, :, :, :] = ig.load_image(side_dir+sampleName, img_channels=img_channels)

					feed_dict = {X_f: test_x_f, X_s: test_x_s, drop: 0}
					test_pred = sess.run(pred, feed_dict)
					test_pred = test_pred[0, :]
					savemat(output_dir+sampleName[:-4]+'.mat', {'pred':test_pred})

		print("Testing Done")
#---------------------------------------------------------------------------------------
def train_or_finetune_UF_US_2(output_path     = '',
					 		  pre_model_path  = '',
						  	  train_files     = '', 
						  	  share_weights   = 0,
						  	  batch_size      = 16,
						  	  nb_epoch        = 50, 
						  	  learning_rate   = 1e-3,
						  	  lr_decay_step   = 0,
						  	  lr_decay_rate   = 0.1,
						  	  img_rows        = 224, 
						  	  img_cols        = 124, 
						  	  img_channels    = 1,
						  	  num_classes     = 26):

	logOutPath = os.path.join(output_path, 'logs')
	if not os.path.exists(logOutPath): os.mkdir(logOutPath)
	LOG_FOUT = open(os.path.join(logOutPath, 'log_train.txt'), 'w')

	graphOutPath = os.path.join(output_path, 'graph')
	if not os.path.exists(graphOutPath): os.mkdir(graphOutPath)

	modelOutPath = os.path.join(output_path, 'model')
	if not os.path.exists(modelOutPath): os.mkdir(modelOutPath)

	with tf.Graph().as_default():
		with tf.device('/gpu:0'):
			# Placeholders
			X_f, X_s, Y, LR, drop = md.placeholder_inputs(img_rows, img_cols, img_channels, num_classes)
			# Construct Network Graph, (batchsize, H, W, Channels)
			pred_op = md.get_UF_US_2_network(X_f, X_s, num_classes, 
											 reuseFlag=bool(share_weights), 
											 drop_rate=drop)
			# Loss
			loss_op = md.get_loss(Y, pred_op)
			#
			tf.summary.scalar('learning_rate', LR)
			tf.summary.scalar('loss', loss_op)

			# Note the global_step=batch parameter to minimize.
			# That tells the optimizer to helpfully increment the 'batch' parameter 
			# for you every time it trains.
			step = tf.Variable(0) # 
			optimizer = tf.train.AdadeltaOptimizer(learning_rate=LR, name='adadelta')
			train_op = optimizer.minimize(loss_op, global_step=step)   

			# Add ops to save and restore all the variables.
			if pre_model_path:
				LOG_FOUT.write('-- load pretrained model from %s \n'%pre_model_path)
				LOG_FOUT.flush()
				sys.stdout.flush()

				saver = tf.train.import_meta_graph(os.path.join(pre_model_path, 'UF-US-2-network.ckpt.meta'))
				saver.restore(sess, os.path.join(pre_model_path, 'UF-US-2-network.ckpt'))
			else:
				saver  = tf.train.Saver()

		# create a session
		config = tf.ConfigProto()
		config.gpu_options.allow_growth = True
		config.allow_soft_placement = True
		config.log_device_placement = True
		sess = tf.Session(config=config)

		# Add summary writers
		merged = tf.summary.merge_all()
		train_writer = tf.summary.FileWriter(graphOutPath, sess.graph)

		# Init variables
		sess.run(tf.global_variables_initializer())

		TRAIN_FILES = ig.getDataFiles(train_files)

		ops = {'X_f' : X_f, 
			   'X_s' : X_s, 
			   'Y'   : Y,
			   'LR'  : LR, 
			   'drop': drop, 
			   'step': step,
			   'pred_op' : pred_op,
			   'loss_op' : loss_op,
			   'train_op': train_op,
			   'merged'  : merged, 
			   'TRAIN_FILES' : TRAIN_FILES,
			   'BATCH_SIZE'  : batch_size}

		for epoch in range(nb_epoch):
			LOG_FOUT.write('------ EPOCH %03d ------\n'%epoch)
			LOG_FOUT.flush()
			sys.stdout.flush()

			# update the learning rate
			if lr_decay_step:
				lr_value = learning_rate * (lr_decay_rate**np.floor(epoch/lr_decay_step))
			else:
				lr_value = learning_rate

			LOG_FOUT.write('--lr = %f ------\n'%lr_value)
			LOG_FOUT.flush()

			train_one_epoch(sess, ops, lr_value, train_writer, LOG_FOUT)

			# save the variables to disk
			if epoch % 10 == 0:
				save_path = saver.save(sess, os.path.join(modelOutPath, 'UF-US-2-network.ckpt'))
				LOG_FOUT.write("Model saved in file: %s \n"%save_path)
				LOG_FOUT.flush()

		# save finale model
		save_path = saver.save(sess. os.path.join(modelOutPath, 'UF-US-2-network.ckpt'))
		LOG_FOUT.write("Model saved in file: %s \n"%save_path)
		LOG_FOUT.flush()
		sys.stdout.flush()

	LOG_FOUT.close()

def train_one_epoch(sess, ops, learning_rate, train_writer, LOG_FOUT):
	# Shuffle train files
	TRAIN_FILES, BATCH_SIZE = ops['TRAIN_FILES'], ops['BATCH_SIZE']

	train_file_idxs = np.arange(0, len(TRAIN_FILES))
	np.random.shuffle(train_file_idxs)

	for fn in range(len(train_file_idxs)):
		LOG_FOUT.write('----- train file Idx : %s -------\n'%str(fn))
		LOG_FOUT.flush()

		data_front, data_side, label = ig.loadDataFile(TRAIN_FILES[train_file_idxs[fn]], shuffleFlag=True)

		file_size = data_front.shape[0]
		num_batches = file_size //BATCH_SIZE

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

		LOG_FOUT.write('mean loss : %f \n'%(loss_sum / float(num_batches)))
		LOG_FOUT.flush()
		#---------------------------------------------------------------------------------------
		# summary = tf.Summary()
		# summary.value.add(tag='epoch_loss', simple_value=val_loss)
		# train_writer.add_summary(summary, iepoch)