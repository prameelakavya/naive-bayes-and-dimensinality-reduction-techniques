import numpy as np
import scipy.linalg as l
import smaiq3

a=[]
b=[]
txt = open('trainlables.txt')
for line in txt:
	line.strip('\n')
#	line=line.split(' ')
	a.append(line)

for i in a:
	j = i.strip('\n')
	a[a.index(i)] = int(j)

#print a
dat= open('train.txt')
for line in dat:
	line.strip('\n')

	line = line.split(' ')
	b.append(line)

for i in b:
	i.pop(-1)

for i in b:
	for j in i:
		b[b.index(i)][i.index(j)] = int(j)

#print b
classone=[]
classtwo=[]
i=0
while(i<100):
	if a[i] == 1:
		classone.append(b[i])
	elif a[i] == -1:
		classtwo.append(b[i])
	i=i+1


#print classtwo
#print '====================='
#print classone

classo = np.array(classone)
classm = np.array(classtwo)

meano = np.mean(classo, axis=0)
meanm = np.mean(classm, axis=0)

del classtwo
del txt
del dat
del classone

datao = classo - meano[np.newaxis,:]
datam = classm - meanm[np.newaxis,:]

scattero = np.dot(datao.transpose(),datao)
scatterm = np.dot(datam.transpose(),datam)

scatterw = scattero + scatterm

mean = meano-meanm
scatterb = np.dot(mean.transpose(), mean)

del meano
del meanm

del classm
del classo
del scattero
del scatterm
print scatterw.shape
#scatterwi = l.inv(scatterw)
#	print scatterwi.shape

eigvec = smaiq3.eigvec[0:-2, :]

sb = np.dot(eigvec, scatterb, eigvec.transpose())
sw = np.dot(eigvec, scatterw, eigvec.transpose())
sinw = l.inv(sw)

sfin = np.dot(sinw, sb)

eival,evec = l.eigh(sfin)

lvec = evec[-1]

reduceddim = np.dot(smaiq3.data,l.transpose())
