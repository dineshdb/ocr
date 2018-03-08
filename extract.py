#!/usr/bin/env python3
import sys
import cv2
import numpy as np
from keras.models import load_model
import scipy.special
import scipy.misc as misc
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf
from predictor import predict
# Create MSER (Maximally Stable External Regions) object
mser = cv2.MSER_create()
#mser.setMinArea(50)
#mser.setMaxArea(800)

image_ratio = 10/30

#pre_trained model with accuracy 83%
model = load_model('my_model.h5')

def draw_contours(img, contours):
    for contour in contours:
        cv2.drawContours(img, [contour], -1, (255, 255, 255), -1)
    return img

def find_texts(url):
    gray = cv2.imread(url, 0)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thres = cv2.adaptiveThreshold(blur,255,1,1,11,2)
    thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)

    mask = np.zeros((gray.shape[0], gray.shape[1], 1), dtype=np.uint8)

    regions, bboxes = mser.detectRegions(thres)
    # [Convex Hull](https://en.wikipedia.org/wiki/Convex_hull) gives the smallest convext set that contains the detected letter
    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

    # Mask and remove all non-text contents
    res = []
#    contour_sizes = [(cv2.contourArea(contour), contour) for contour in regions]
#    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    for coor in regions:
        bbox = cv2.boundingRect(coor)
        x, y, w, h = bbox
        cv2.rectangle(thres, (x, y), (x+w, y+h), (255, 0, 0), 1)
        letter = thres[y:y+h, x:x+w]
        resized = misc.imresize(letter,(28,28))

        img_array = np.array(resized)
        reshaped = img_array.reshape(1, 1,28,28)
        new = np.array(reshaped)

        label = model.predict(new)
        prediction = get_label(np.argmax(label,axis=1)[0])
        res.append({"x" : x, "y" : y, "label": prediction})
        
    print(res)
      
    cv2.imshow("img", thres)
    cv2.waitKey(0)

    return res
    
print(find_texts("images/a.jpg"))
