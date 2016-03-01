#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scipy.spatial.distance import pdist, squareform, cdist
import scipy
import numpy as np
import math


def getDimensionReducedData(m, kernel_mat, k, type, dataSet):
	dimReducedData = m.T.dot(kernel_mat)
	np.savetxt(dataSet + '_' + type + '_' + str(k) + '.data', dimReducedData.T)


def kernelPCA(trainFile, validationFile, gamma, k1, k2):

	data = np.loadtxt(open(trainFile))
	validationData = np.loadtxt(open(validationFile))

	print "Read training and validation data from files."

	sq_distances = squareform(pdist(data, 'sqeuclidean'))
	kernel_mat = np.exp(-1 * gamma * sq_distances)

	print "Kernel Matrix Computed."

	mat_oneByN = np.ones(kernel_mat.shape) / kernel_mat.shape[0]
	kernelCentered_mat = kernel_mat - (mat_oneByN.dot(kernel_mat)) - (kernel_mat.dot(mat_oneByN)) + \
						(mat_oneByN.dot(kernel_mat).dot(mat_oneByN))

	print "Centered Kernel Matrix."

	eigenvalues, eigenvectors = np.linalg.eigh(kernelCentered_mat)

	eig_pairs = [(eigenvalues[i], eigenvectors[i]) for i in range(len(eigenvalues))]

	eig_pairs = sorted(eig_pairs, key = lambda x: x[0])
	eig_pairs.reverse()

	print "Eigenvalues and Eigenvectors calculated."

	matrix_W_k1 = np.hstack(tuple([(eig_pairs[i][1].reshape(-1, 1) / eig_pairs[i][0]) for i in range(k1)]))
	matrix_W_k2 = np.hstack(tuple([(eig_pairs[i][1].reshape(-1, 1) / eig_pairs[i][0]) for i in range(k2)]))

	getDimensionReducedData(matrix_W_k1, kernel_mat, k1, 'train', trainFile.split('_')[0])
	getDimensionReducedData(matrix_W_k2, kernel_mat, k2, 'train', trainFile.split('_')[0])

	sq_distances_valid = cdist(data, validationData, 'sqeuclidean')
	kernel_mat_valid = np.exp(-1 * gamma * sq_distances_valid)

	getDimensionReducedData(matrix_W_k1, kernel_mat_valid, k1, 'valid', trainFile.split('_')[0])
	getDimensionReducedData(matrix_W_k2, kernel_mat_valid, k2, 'valid', trainFile.split('_')[0])

	print "Finished."


if __name__ == "__main__":
	kernelPCA('arcene/arcene_train.data', 'arcene/arcene_valid.data', 0.000000001, 10, 100)
	#kernelPCA('heart/SPECTF_train.data', 'heart/SPECTF_test.data', (1.0 / (44.0 * 44.0)), 10, 30)