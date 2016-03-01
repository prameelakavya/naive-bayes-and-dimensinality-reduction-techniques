from sklearn.naive_bayes import GaussianNB
import numpy as np
import a , reduceddim from a
import reddim from smaiq3
model = GaussianNB()

model.fit(reduceddim, a)

predicted= model.predict(reduceddim)

print predicted
