#!/usr/bin/env python3
import sys
import cv2
import numpy as np

# Create MSER (Maximally Stable External Regions) object
mser = cv2.MSER_create()
#mser.setMinArea(50)
#mser.setMaxArea(800)

image_ratio = 10/30

def draw_contours(img, contours):
    for contour in contours:
        cv2.drawContours(img, [contour], -1, (255, 255, 255), -1)
    return img
    
def find_texts(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thres = cv2.adaptiveThreshold(blur,255,1,1,11,2)
#    thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 11, 2)
  
    mask = np.zeros((img.shape[0], img.shape[1], 1), dtype=np.uint8)
   
    regions, bboxes = mser.detectRegions(thres)
    # [Convex Hull](https://en.wikipedia.org/wiki/Convex_hull) gives the smallest convext set that contains the detected letter
    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

    # Mask and remove all non-text contents
#    mask = draw_contours(thres, regions)        
#    text_only = cv2.bitwise_and(thres, thres, mask=mask)

    hulls = []
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in regions]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    for coor in regions:
        bbox = cv2.boundingRect(coor)
        hull = cv2.convexHull(coor.reshape(-1, 1, 2))
        x, y, w, h = bbox
        cv2.rectangle(thres, (x, y), (x+w, y+h), (255, 0, 0), 1)
        text = img[y:y+h, x:x+w]
        hulls.append(bbox)
#        cv2.drawContours(img, [hull], -1, (255, 255, 255), -1)
        
    result = thres

    cv2.imshow("orig", result)
    while cv2.waitKey(0) != 27:
        pass
    cv2.destroyAllWindows()
    
    
img = cv2.imread("img/2.jpg")
find_texts(img)
