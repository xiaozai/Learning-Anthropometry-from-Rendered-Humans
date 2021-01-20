import cv2
import os
import numpy as np
from scipy.io import loadmat

import argparse
parser = argparse.ArgumentParser(description='Generate synth dataset images.')
parser.add_argument('--startIdx', type=int)
parser.add_argument('--endIdx',   type=int)
parser.add_argument('--imgDir', default='')
parser.add_argument('--matDir', default='')
parser.add_argument('--outDir', default='')

if __name__ == '__main__':
	
	args = parser.parse_args()

	sampleList = os.listdir(args.imgDir+'front/')

	for idx in range(args.startIdx, args.endIdx):
		sName = sampleList[idx][:-4]

		matInfo = loadmat(args.matDir+sName+'.mat')['bg'][0]
		bgI = cv2.imread(matInfo)

		frontI = cv2.imread(args.imgDir+'front/'+sName+'.png')
		frontDiff = frontI - bgI
		frontMask = np.any(frontDiff, axis=2)
		cv2.imwrite(args.outDir+'front/'+sName+'.png', frontMask*255)

		sideI = cv2.imread(args.imgDir+'side/'+sName+'.png')
		sideDiff = sideI - bgI
		sideMask = np.any(sideDiff, axis=2)
		cv2.imwrite(args.outDir+'side/'+sName+'.png', sideMask*255)

	print("Done")