import os
import sys
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
import cv2
import numpy as np
from keras.models import load_model
import scipy.special
import scipy.misc as misc

# Create MSER (Maximally Stable External Regions) object
mser = cv2.MSER_create()
#mser.setMinArea(50)
#mser.setMaxArea(800)

#pre_trained model with accuracy 83%
model = load_model('my_model.h5')
model._make_predict_function()
graph = tf.get_default_graph()

#get the label from index 
def get_label(index):
    if index < 26:
        label = index + 65
    else:
        index=index%26
        label = index + 97
    return chr(label)


#predictor function
def predict(addr):
	img = misc.imread(addr,flatten=True)
	img_array= misc.imresize(img,(28,28))

	img = img_array.reshape(1,28,28)
	new = [img]*2

	new = np.array(new)
	out = model.predict(new)
	prediction = get_label((np.argmax(out,axis=1))[0])
	return prediction

def find_texts(url):
    gray = cv2.imread(url, 0)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thres = cv2.adaptiveThreshold(blur,255,1,1,11,2)
    thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)

    mask = np.zeros((gray.shape[0], gray.shape[1], 1), dtype=np.uint8)

    regions, bboxes = mser.detectRegions(thres)

    # Mask and remove all non-text contents
    res = []
#    contour_sizes = [(cv2.contourArea(contour), contour) for contour in regions]
#    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    for coor in regions:
        bbox = cv2.boundingRect(coor)
        x, y, w, h = bbox
        cv2.rectangle(thres, (x, y), (x+w, y+h), (255, 0, 0), 1)
        letter = thres[y:y+h, x:x+w]

        resized = cv2.resize(letter,(28,28))

#        img_array = np.array(resized)
#        new = img_array.reshape(1, 1,28,28)

        img = resized.reshape(1,28,28)
        new = [img]*2

        new = np.array(new)
        with graph.as_default():
            label = model.predict(new)
        prediction = get_label(np.argmax(label,axis=1)[0])
        res.append({"coor" : bbox, "label": prediction})

    return res

#print(find_texts("images/a.jpg"))
