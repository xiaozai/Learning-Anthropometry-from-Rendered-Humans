import numpy as np
from scipy.io import loadmat
import imageio
import h5py
#--------------------------------------------------------------------------------------------
def load_image(fname, img_channels=3):
	img = imageio.imread(fname)  # H*W*C
	if img_channels==1:
		img = np.expand_dims(img, -1) # H*W*1
	return img

def loadDataFile(filename, shuffleFlag=True):
	return load_h5(filename, shuffleFlag)

def getDataFiles(list_filename):
	return [line.strip() for line in open(list_filename)]

def load_h5(h5_filename, shuffleFlag=True):
	f = h5py.File(h5_filename)
	print(h5_filename)
	data_front = f['data_front'][:]
	data_side  = f['data_side'][:]
	label      = f['label'][:]

	idx = np.arange(len(label))
	if shuffleFlag:
		np.random.shuffle(idx)

	return (data_front[idx, ...], data_side[idx, ...], label[idx, ...])

def loadDataFile_onlyLength(filename, shuffleFlag=True):
	return load_h5_onlyLength(filename, shuffleFlag)

def load_h5_onlyLength(h5_filename, shuffleFlag=True):
	f = h5py.File(h5_filename)
	data_front = f['data_front'][:]
	data_side  = f['data_side'][:]
	label      = f['label'][:]

	label_onlyLength = np.zeros((len(label), 5), dtype=np.float32)
	label_onlyLength[:, 0] = label[:, 2]  # shoulder-blade length
	label_onlyLength[:, 1] = label[:, 9]  # arm length
	label_onlyLength[:, 2] = label[:, 10] # inside leg length
	label_onlyLength[:, 3] = label[:, 14] # overall height
	label_onlyLength[:, 4] = label[:, 15] # shoulder breadth

	idx = np.arange(len(label))
	if shuffleFlag:
		np.random.shuffle(idx)

	return (data_front[idx, ...], data_side[idx, ...], label_onlyLength[idx, ...])

def loadDataFile_onlyHeight(filename, shuffleFlag=True):
	return load_h5_onlyHeight(filename, shuffleFlag)

def load_h5_onlyHeight(h5_filename, shuffleFlag=True):
	f = h5py.File(h5_filename)
	data_front = f['data_front'][:]
	data_side  = f['data_side'][:]
	label      = f['label'][:]

	label_onlyLength = np.zeros((len(label), 1), dtype=np.float32)
	label_onlyLength[:, 0] = label[:, 14] # overall height

	idx = np.arange(len(label))
	if shuffleFlag:
		np.random.shuffle(idx)

	return (data_front[idx, ...], data_side[idx, ...], label_onlyLength[idx, ...])

def loadDataFile_onlyChest(filename, shuffleFlag=True):
	return load_h5_onlyChest(filename, shuffleFlag)

def load_h5_onlyChest(h5_filename, shuffleFlag=True):
	f = h5py.File(h5_filename)
	data_front = f['data_front'][:]
	data_side  = f['data_side'][:]
	label      = f['label'][:]

	label_onlyChest = np.zeros((len(label), 1), dtype=np.float32)
	label_onlyChest[:, 0] = label[:, 3] # chest circ

	idx = np.arange(len(label))
	if shuffleFlag:
		np.random.shuffle(idx)

	return (data_front[idx, ...], data_side[idx, ...], label_onlyChest[idx, ...])

def loadDataFile_onlyCirc(filename, shuffleFlag=True):
	return load_h5_onlyCirc(filename, shuffleFlag)

def load_h5_onlyCirc(h5_filename, shuffleFlag=True):
	f = h5py.File(h5_filename)
	data_front = f['data_front'][:]
	data_side  = f['data_side'][:]
	label      = f['label'][:]

	label_onlyCirc = np.zeros((len(label), 11), dtype=np.float32)
	label_onlyCirc[:, 0] = label[:, 0]  
	label_onlyCirc[:, 1] = label[:, 1]  
	label_onlyCirc[:, 2] = label[:, 3]
	label_onlyCirc[:, 3] = label[:, 4] 
	label_onlyCirc[:, 4] = label[:, 5] 
	label_onlyCirc[:, 5] = label[:, 6]
	label_onlyCirc[:, 6] = label[:, 7] 
	label_onlyCirc[:, 7] = label[:, 8] 
	label_onlyCirc[:, 8] = label[:, 11] 
	label_onlyCirc[:, 9] = label[:, 12] 
	label_onlyCirc[:, 10] = label[:, 13] 

	idx = np.arange(len(label))
	if shuffleFlag:
		np.random.shuffle(idx)

	return (data_front[idx, ...], data_side[idx, ...], label_onlyCirc[idx, ...])
# #-----------------------------------------------------------------------------------------
# def load_label(fname):
# 	y = loadmat(fname)['y'][0]
# 	return y
# #------------------------------------------------------------------------------------------
# def load_batch(filePathX_front, 
# 			   filePathX_side,
# 			   filePathY, 
# 			   sampleNameList, 
# 			   batch_idx, 
# 			   batch_size=32, 
# 			   output_parameters=10,
# 			   img_rows=480, 
# 			   img_cols=320, 
# 			   img_channels=3):

# 	max_num   = len(sampleNameList)
# 	samplesID = range(batch_idx*batch_size, (batch_idx+1)*batch_size)
# 	samplesID = np.mod(samplesID, max_num)

# 	x_front = np.zeros((batch_size, img_rows, img_cols, img_channels), dtype=float)
# 	x_side  = np.zeros((batch_size, img_rows, img_cols, img_channels), dtype=float)
# 	y       = np.zeros((batch_size, output_parameters), dtype=float)

# 	for j in range(batch_size):
# 		sampleName = sampleNameList[samplesID[j]]
# 		sampleName = str(sampleName.decode('utf-8'))
		
# 		x_front[j, :, :, :] = load_image(filePathX_front+sampleName+'.png', img_channels=img_channels)
# 		x_side[j, :, :, :]  = load_image(filePathX_side +sampleName+'.png', img_channels=img_channels)
# 		y[j, :]             = load_label(filePathY+sampleName+'.mat')

# 	return x_front, x_side, y
# #------------------------------------------------------------------------------------------