import tensorflow as tf
import cv2
import numpy as np
from keras.models import load_model
import scipy.misc as misc

# Create MSER (Maximally Stable External Regions) object
mser = cv2.MSER_create()

# pre_trained model with accuracy 83%
model = load_model('my_model.h5')
model._make_predict_function()
graph = tf.get_default_graph()


# get the label from index
def get_label(index):
    if index < 26:
        label = index + 65
    else:
        index = index % 26
        label = index + 97
    return chr(label)


# predictor function
def predict(addr):
    img = misc.imread(addr, flatten=True)
    img_array = misc.imresize(img, (28, 28))

    img = img_array.reshape(1, 28, 28)
    new = [img] * 2

    new = np.array(new)
    out = model.predict(new)
    prediction = get_label((np.argmax(out, axis=1))[0])
    return prediction


def draw_contours(img, contours):
    cv2.polylines(img, contours, 1, (0, 255, 0))
    for contour in contours:
        cv2.drawContours(img, [contour], -1, (255, 255, 255), -1)
    return img


def find_texts(img, min, max):
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    thres = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)
    mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
    regions = mser.detectRegions(thres, None)
    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
    mask = draw_contours(mask, hulls)
    extract = cv2.bitwise_and(thres, thres, mask=mask)

    regions = np.asarray([cv2.boundingRect(part) for part in regions])

    _, _, maxWidth, maxHeight = np.amax(regions, 0)
    _, _, minWidth, minHeight = np.amin(regions, 0)
    testWidth = (maxWidth + minWidth) // 2

    string = " "

    # regions.view('uint8,uint8,uint8,uint8').sort(order=['f1'], axis=0)
    xx, yy, ww, hh = regions[0]
    i = 0
    res = []
    for part in regions:
        x, y, w, h = part
        if abs(x - xx) < minWidth:
            continue
        text = extract[y:y + h, x:x + w]
        text = text
        letter = np.zeros((h, h), dtype=np.uint8)

        if h > w:
            gap = (h - w) // 2
            letter[0: h, gap: gap + w] = text
        else:
            letter = np.zeros((w, w), dtype=np.uint8)
            gap = (w - h) // 2
            letter[gap: gap + h, 0: w] = text

        letter = cv2.resize(letter, (40, 40), interpolation=cv2.INTER_CUBIC)

        letter1 = np.zeros((50, 50), dtype=np.uint8)
        letter1[5:45, 5:45] = letter
        letter = cv2.resize(letter1, (28, 28), interpolation=cv2.INTER_AREA)
        letter = cv2.bitwise_not(letter1)
        img = letter.reshape(1, 28, 28)
        new = np.asarray([img] * 2)

        with graph.as_default():
            label = model.predict(new)
        prediction = get_label(np.argmax(label, axis=1)[0])

        if abs(x - xx - w) > testWidth:
            string = string + ' '
        string = string + prediction

        xx, yy, ww, hh = part

    return string

