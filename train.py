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
import glob 

#CNN model
def Model():
    # create model
    model = Sequential()
    model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(15, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(50, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

#training the dataset
#although the main directory contains datasets for digits, but this model trains only the characters. 
directory = str() #provide the main directory 
main_path = glob.glob(directory)
p = str()
count = 0
csv_dataset = []
label = 0
total = 0
for x in main_path:
    path = glob.glob(x+'/*')
    for addrs in path:
        addrs = glob.glob(addrs+'/*')
        for addr in addrs:
            img = misc.imread(addr,flatten=True)
            img_array= misc.imresize(img,(28,28))
            img_data = img_array.reshape(784)
            record = np.append(label,img_data)
            csv_dataset.append(record)
            total+=1
        label+=1
    label = 0
#saving the dataset image arrays in csv file
array_of_csv_dataset = np.array(csv_dataset)
array_of_csv_dataset = array_of_csv_dataset.reshape((total,785))
np.random.shuffle(array_of_csv_dataset)
np.savetxt("dataset.csv",array_of_csv_dataset,fmt = '%d',delimiter = ',',newline = ' \n')



#csv dataset of 74K samples
dataset_file = open("dataset.csv",'r')
dataset_list = dataset_file.readlines()
dataset_file.close()

#training dataset and test dataset in ratio 8:2
training_dataset_list = dataset_list[0:int(0.8*len(dataset_list))]
test_dataset_list = dataset_list[int(0.8*len(dataset_list))+1:]

X_train = []
Y_train = []
X_test = []
Y_test = []

for record in training_dataset_list:
        all_values = record.split(',')
        inputs = (np.asfarray(all_values[1:]))
        X_train.append(inputs.reshape(28,28))
        Y_train.append((all_values[0]))


X_train = np.array(X_train)
X_train = X_train.reshape(X_train.shape[0],28,28)
Y_train = np.array(Y_train)

X_test = []
Y_test = []
for record in test_dataset_list:
        all_values = record.split(',')
        inputs = (np.asfarray(all_values[1:]))
        X_test.append(inputs.reshape(28,28))
        Y_test.append(np.asfarray(all_values[0]))
X_test = np.array(X_test)
Y_test = np.array(Y_test)


K.set_image_dim_ordering('th')
# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# reshape to be [samples][pixels][width][height]
X_train = X_train.reshape(X_train.shape[0], 1, 28, 28).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1, 28, 28).astype('float32')
# normalize inputs from 0-255 to 0-1//
X_train = X_train / 255
X_test = X_test / 255
# one hot encode outputs
Y_train = np_utils.to_categorical(Y_train)
Y_test = np_utils.to_categorical(Y_test)
num_classes = Y_test.shape[1]

#defining the model
model = Model()

#fitting the dataset in model
epoch = 10
model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=epoch, batch_size=200)
# Final evaluation of the model
scores = model.evaluate(X_test, Y_test, verbose=0)
print("Large CNN Error: %.2f%%" % (100-scores[1]*100))

model.save('my_model.h5')
del model
