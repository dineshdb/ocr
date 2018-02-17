#!/usr/bin/env python3
import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Create MSER (Maximally Stable External Regions) object
mser = cv2.MSER_create()

def draw_contours(img, contours):
    cv2.polylines(img, contours, 1, (0, 255, 0))
    for contour in contours:
        cv2.drawContours(img, [contour], -1, (255, 255, 255), -1)
    return img
    
def find_texts(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thres = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)

    mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
    
    regions, _ = mser.detectRegions(thres)

    # [Convex Hull](https://en.wikipedia.org/wiki/Convex_hull) gives the smallest convext set that contains the detected letter
    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
    
    # Mask and remove all non-text contents
    mask = draw_contours(mask, hulls)        
    text_only = cv2.bitwise_and(thres, thres, mask=mask)

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    
    plt.subplot(121),plt.imshow(img),plt.title('Original')
    plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(text_only),plt.title('Blurred')
    plt.xticks([]), plt.yticks([])
    plt.show()
    
img = cv2.imread("img/1.jpg")
find_texts(img)
