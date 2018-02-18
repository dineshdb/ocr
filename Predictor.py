import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.models import load_model
import scipy.special
import scipy.misc as misc
import matplotlib.pyplot as plt





#pre_trained model with accuracy 83%
model = load_model('model.h5')

#get the label from index 
def get_label(index):
    if index < 26:
        label = index + 65    
    else:
        index=index%26
        label = index + 97
    return chr(label)


#predictor function
def predict(path):
	addr = path
	img = misc.imread(addr,flatten=True)
	img_array= misc.imresize(img,(28,28))
	img = img_array.reshape(1,28,28)
	new = [img]*2
	new = np.array(new)
	out = model.predict(new)
	prediction = get_label((np.argmax(out,axis=1))[0])
	return (prediction)
#prediction of the single test data

print(predict('c.jpg'))



