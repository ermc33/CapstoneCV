
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 19:07:23 2017

@author: ernes
"""

import cv2
import numpy as np

#Initialize variables
contour_List = []
drawing = np.zeros([400, 630],np.uint8)
centres = []

#Read torpedo image
image = cv2.imread('Torpedo.jpg')
image = cv2.resize(image,(630,400))
cv2.imshow('Target',image)

#Apply Bilateral Filter to smooth the image and reduce noise
image = cv2.bilateralFilter(image,3,500,500)

#Apply color processing to the filtered image
lower = np.array([0,0,0], dtype='uint8')
upper = np.array([0,200,200], dtype='uint8')
#thresh = np.array([255,255,105], dtype='uint8') 
output_image = cv2.inRange(image, lower, upper)
cv2.imshow('output', output_image)

#Calculate edges and display it on the edge map
edges = cv2.Canny(image, 0,100, True)
cv2.imshow('edges', edges)

#Look for contours similar to a rectangle and save them
contours, _ = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    if 4 <= len(approx) <= 6: 
        contour_List.append(contour)
#        x,y,w,h = cv2.boundingRect(approx)

#Draw the contours on a new image and calulate the center of each one
for i in xrange(len(contour_List)):
    cv2.drawContours(drawing, contour_List,  -1, (255), 2)
    moments = cv2.moments(contour_List[i])
    centres.append((int(moments['m10']/moments['m00']),int(moments['m01']/moments['m00'])))
    cv2.circle(drawing, centres[-1], 7, (255, 255, 255), -1)
cv2.imshow('contours', drawing)

#Sort centers from lowest to highest in terms of x and y to determine which is which
centres = list(set(centres))
centres = sorted(centres)

#Eliminate repeated centers and create list with only 5 centers
#one for the big yellow rectangle and one for each opening (4 in total)
areas = [cv2.contourArea(c) for c in contour_List]
areasDes = sorted(areas,reverse = True)
areasDes = list(set(areasDes)) 


    
