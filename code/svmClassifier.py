#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sklearn import svm
import numpy as np

def classify(trainDataFile, validDataFile, trainLabelsFile, validLabelsFile, k):

	trainData = np.loadtxt(open(trainDataFile))
	validationData = np.loadtxt(open(validDataFile))
	trainLabels = np.loadtxt(open(trainLabelsFile))
	validLabels = np.loadtxt(open(validLabelsFile))

	trainData = np.reshape(trainData, (trainLabels.shape[0], -1))
	validationData = np.reshape(validationData, (validLabels.shape[0], -1))

	clf_rbf = svm.SVC(kernel = 'rbf')
	clf_linear = svm.SVC(kernel = 'linear')

	clf_rbf.fit(trainData, trainLabels)
	clf_linear.fit(trainData, trainLabels)

	correct_rbf = 0.0
	correct_linear = 0.0

	for ind, i in enumerate(validationData):
		result_rbf = clf_rbf.predict(i)
		result_linear = clf_linear.predict(i)
		
		if result_rbf[0] == validLabels[ind]:
			correct_rbf += 1

		if result_linear[0] == validLabels[ind]:
			correct_linear += 1


	accuracy_rbf = (correct_rbf / len(validLabels)) * 100
	accuracy_linear = (correct_linear / len(validLabels)) * 100

	print "Accuracy for SVM with RBF kernel for K =", k, ":", accuracy_rbf
	print "Accuracy for SVM with linear kernel for K =", k, ":", accuracy_linear


if __name__ == "__main__":

	print "DataSet: Arcene"
	classify('arcene/arcene_train_1.data', 'arcene/arcene_valid_1.data', 'arcene/arcene_train.labels', 'arcene/arcene_valid.labels', 1)
	classify('arcene/arcene_train_10.data', 'arcene/arcene_valid_10.data', 'arcene/arcene_train.labels', 'arcene/arcene_valid.labels', 10)
	#classify('arcene/arcene_train_100.data', 'arcene/arcene_valid_100.data', 'arcene/arcene_train.labels', 'arcene/arcene_valid.labels', 100)

	# print "DataSet: Heart(SPECTF)"
	# classify('heart/SPECTF_train_1.data', 'heart/SPECTF_valid_1.data', 'heart/SPECTF_train.labels', 'heart/SPECTF_test.labels', 1)
	# classify('heart/SPECTF_train_10.data', 'heart/SPECTF_valid_10.data', 'heart/SPECTF_train.labels', 'heart/SPECTF_test.labels', 10)
	# classify('heart/SPECTF_train_30.data', 'heart/SPECTF_valid_30.data', 'heart/SPECTF_train.labels', 'heart/SPECTF_test.labels', 30)