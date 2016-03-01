import numpy as np
import scipy.linalg as l

data = np.loadtxt("train.txt")
mean = np.mean(data, axis=0)
data - mean[np.newaxis,:]
scatter = np.dot(data.transpose(),data)
eigval,eigvec = l.eigh(scatter)
final = np.split(eigvec,10)
finalk = final[-1]
reddim = np.dot(data,finalk.transpose())
