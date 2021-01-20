import numpy as np
from scipy.io import loadmat
import argparse
import os
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('--prediction_path',    default='')
parser.add_argument('--label_path',         default='')
parser.add_argument('--log_path',           default='')
parser.add_argument('--num_meas', type=int, default=5)
parser.add_argument('--pred_type',type=int, default=1, help='1 for pred , 2 for y')
FLAGS = parser.parse_args()

PRED_PATH  = FLAGS.prediction_path
LABEL_PATH = FLAGS.label_path
NUM_MEAS   = FLAGS.num_meas
PRED_TYPE  = FLAGS.pred_type

LOG_PATH = FLAGS.log_path
if not os.path.exists(LOG_PATH): os.mkdir(LOG_PATH)
LOG_FOUT = open(os.path.join(LOG_PATH, 'log_mae.txt'), 'w')

def log_string(out_str):
	LOG_FOUT.write(out_str+'\n')
	LOG_FOUT.flush()

def main():
	
	sampleList = os.listdir(PRED_PATH)
	nSamples = len(sampleList)
	log_string('Totally %d samples'%nSamples)

	MAE = np.zeros((nSamples, NUM_MEAS), dtype=np.float32)

	for ii in range(nSamples):
		sname = sampleList[ii]
		if PRED_TYPE == 1:
			pred = loadmat(os.path.join(PRED_PATH, sname))['pred'][0]
		elif PRED_TYPE ==2:
			pred = loadmat(os.path.join(PRED_PATH, sname))['y'][0]

		Y = loadmat(os.path.join(LABEL_PATH, sname))['y'][0]
		NewY = np.zeros((NUM_MEAS,), dtype=np.float32)
		if NUM_MEAS == 5:
			NewY[0] = Y[2]
			NewY[1] = Y[9]
			NewY[2] = Y[10]
			NewY[3] = Y[14]
			NewY[4] = Y[15]
		elif NUM_MEAS == 11:
			NewY[0] = Y[0]
			NewY[1] = Y[1]
			NewY[2] = Y[3]
			NewY[3] = Y[4]
			NewY[4] = Y[5]
			NewY[5] = Y[6]
			NewY[6] = Y[7]
			NewY[7] = Y[8]
			NewY[8] = Y[11]
			NewY[9] = Y[12]
			NewY[10] = Y[13]
		elif NUM_MEAS == 1:
			NewY[0] = Y[3] # only chest circ
		else:
			NewY = Y

		meas_error = abs(NewY - pred)
		for jj in range(NUM_MEAS):
			if meas_error[jj] > 20:
				print('%s : %d-th meas error is %f'%(sname, jj, meas_error[jj]))

		MAE[ii, :] = meas_error
	
	# plot hist of mae 
	# for ii in range(NUM_MEAS):
	# 	meas_mae = MAE[:, ii]
	# 	plt.figure()
	# 	plt.hist(meas_mae)
	# 	plt.show()

	average_mae = np.mean(MAE, 0)
	log_string('MAE = ')
	for m in average_mae:
		log_string('-- %f'%m)
	average_MAE = np.mean(average_mae)
	log_string('average MAE = %f'%average_MAE)

if __name__ == '__main__':
	main()
	LOG_FOUT.close()