#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.spatial.distance import pdist, squareform, cdist
import scipy
import numpy as np
import math


def getDimensionReducedData(m, kernel_mat, k, type, dataSet):
	dimReducedData = m.T.dot(kernel_mat)
	np.savetxt(dataSet + '_' + type + '_' + str(k) + '.data', dimReducedData.T)


def getKernelMatrix(data, gamma):

	sq_distances = squareform(pdist(data, 'sqeuclidean'))
	kernel_mat = np.exp(-1 * gamma * sq_distances)

	mat_oneByN = np.ones(kernel_mat.shape) / kernel_mat.shape[0]
	kernelCentered_mat = kernel_mat - (mat_oneByN * kernel_mat) - (kernel_mat * mat_oneByN) + (mat_oneByN * kernel_mat * mat_oneByN)

	return (kernel_mat, kernelCentered_mat)


def kernelLDA(trainFile, validFile, labelsFile, gamma):

	trainData = np.loadtxt(open(trainFile))
	validationData = np.loadtxt(open(validFile))
	labels = np.loadtxt(open(labelsFile))

	print "Read training and validation data from files..."

	class1 = []
	class2 = []

	for i in range(len(labels)):
		if labels[i] == 1:
			class1.append(trainData[i])
		else:
			class2.append(trainData[i])

	class1 = np.vstack(tuple(class1))
	class2 = np.vstack(tuple(class2))

	data = np.concatenate((class1, class2))

	kernel_mat, kernelCentered_mat = getKernelMatrix(data, gamma)

	print "Kernel matrix obtained."

	K1 = np.vsplit(kernelCentered_mat, [class1.shape[0], data.shape[0]])[0]
	K2 = np.vsplit(kernelCentered_mat, [class1.shape[0], data.shape[0]])[1]

	mat_N1 = K1.T.dot( \
	 		(np.identity(K1.shape[0]) - (np.ones((K1.shape[0], K1.shape[0])) / K1.shape[0]))).dot( \
	 		K1)

	mat_N2 = K2.T.dot( \
	 		(np.identity(K2.shape[0]) - (np.ones((K2.shape[0], K2.shape[0])) / K2.shape[0]))).dot( \
	 		K2)

	N = mat_N1 + mat_N2

	M1 = np.average(K1, axis = 0)
	M2 = np.average(K2, axis = 0)

	#alpha = np.linalg.inv(N).dot(M2 - M1)
	alpha = (M2 - M1)

	getDimensionReducedData(alpha, kernelCentered_mat, 1, 'train', trainFile.split('_')[0])

	sq_distances_valid = cdist(data, validationData, 'sqeuclidean')
	kernel_mat_valid = np.exp(-1 * gamma * sq_distances_valid)

	getDimensionReducedData(alpha, kernel_mat_valid, 1, 'valid', trainFile.split('_')[0])

	print "Finished."



if __name__ == "__main__":
	kernelLDA('arcene/arcene_train.data', 'arcene/arcene_valid.data', 'arcene/arcene_train.labels', 0.000000001)
	#kernelLDA('heart/SPECTF_train.data', 'heart/SPECTF_test.data', 'heart/SPECTF_train.labels', (1.0 / (44.0 * 44.0)))