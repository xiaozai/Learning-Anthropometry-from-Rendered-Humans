import numpy as np
import os
import pickle
from scipy.io import loadmat, savemat
from sklearn.linear_model import LinearRegression


def train():
	gender = 'male'
	dataDir = '/home/yan/Data2/narvi_folder/Pre-Process-CAESARfits/CAESAR-Fits01/%s-synthetic-samples/'%gender
	measDir = dataDir + '20D-PCA/meas/group01/26D-Meas-Labels/'
	pcaDir = dataDir + '20D-PCA/mat/group01/'

	sampleList = os.listdir(pcaDir)
	nsamples = len(sampleList)
	print('totally %d samples'%nsamples)

	measArray = np.zeros((nsamples, 26), dtype=np.float32)
	pcaArray = np.zeros((nsamples, 20), dtype=np.float32)

	for ii in range(nsamples):
		pca = loadmat(pcaDir+sampleList[ii])
		meas = loadmat(measDir+sampleList[ii])

		pcaArray[ii, :] = pca['score'][0]
		measArray[ii, :] = meas['y'][0]

	outDir = '/home/yan/Desktop/demo_for_CPU_test/Regressor_From_Meas_To_ShapeParameters/'
	savemat(outDir+'regressor_trainingData.mat', {'pcaData': pcaArray, 'measData':measArray})

	# Train Regressor
	regressor = LinearRegression().fit(measArray, pcaArray)

	with open(outDir + 'CAESAR-Fits01-%s-26D-Meas-20D-PCA-Group01-LinearRegressionModel.pkl'%gender, 'wb') as file:
		pickle.dump(regressor, file)

def test():
	gender = 'male'
	dataDir = '/home/yan/Desktop/demo_for_CPU_test/Regressor_From_Meas_To_ShapeParameters/'
	regressorfile = dataDir+ 'CAESAR-Fits01-%s-26D-Meas-20D-PCA-Group01-LinearRegressionModel.pkl'%gender

	with open(regressorfile, 'rb') as file:
		regressor = pickle.load(file)

	testData = [592.25714, 368.515, 958.7056, 877.17816, 881.14703, 954.7173, 
				981.13275, 569.0949, 53.0229, 356.21085, 217.74551, 275.17133,
				244.53899, 248.49731, 155.48154, 241.4315, 40.785156, 405.96637,
				505.15176, 166.43494, 378.7466, 363.7604, 277.69858, 246.68922,
				179.30322, 243.66858]

	# [603.3816   358.54578  934.12225  844.5071   848.4218   939.29596
	#  969.4864   553.8243   350.73703  348.63675  215.44057  260.18536
	#  234.43156  240.06227  149.23854  241.75696   43.274166 405.32297
	#  510.72305  172.4453   396.7939   379.83078  288.5062   257.13452
	#  183.54547  246.61052 ]

	testData = np.asarray(testData)
	testData = testData.reshape(1, -1)
	print(testData.shape)  # (1, 26)

	predPCA = regressor.predict(testData)
	print(predPCA.shape)   # (1, 20)
	predPCA = predPCA[0]
	print(predPCA)

	predPCA = [max(x, -2) for x in predPCA]
	predPCA = [min(x, 2) for x in predPCA]
	print(predPCA)


if __name__ == '__main__':

	# train()

	test()