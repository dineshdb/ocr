import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

import numpy as np

from keras.models import load_model
import scipy.special
import scipy.misc as misc


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
print(predict('images/c.jpg'))

#prediction of the single test data

