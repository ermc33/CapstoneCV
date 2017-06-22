#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 13:35:57 2017

@author: Edwin
"""

import cv2
import numpy as np


contour_ListGate = [] 
contoursY = np.array([])
contoursYnew = []
hierarchy_Y = np.array([])
contour_ListY = [] 
centres = []
rectList = []
YgateIm = cv2.imread("GateSIM.jpg")
YgateIm= cv2.resize(YgateIm, (630,400))
Filt_Ygate = cv2.bilateralFilter(YgateIm,7,900,900)
'Color Thresholds'
lower_thresh = np.array([0,0,0], dtype='uint8') #Parameter to adjust in the pool
upper_thresh = np.array([20,255,255 ], dtype='uint8')#Parameter to adjust in the pool
'Image Segmentation'
segmented_image = cv2.inRange(Filt_Ygate , lower_thresh, upper_thresh) 
'Calculate Edge Map'
Ygate_edges = cv2.Canny(Filt_Ygate, 10,100, True)
'Find Contours'
contoursY, hierarchy_Y = cv2.findContours(Ygate_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, contoursY, hierarchy_Y )
if len(contoursY) ==0:
    print "Adjust canny"
#    

'Look for a rectangle'
for contour in contoursY:
    approxV = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour,True),True)
    if (len(approxV) >= 3 and len(approxV) <= 6 ):
    #if (( 4 <= len(approxV) <= 10)) :
        contour_ListGate.append(contour)
'Check if rectangle were found'        
if len(contour_ListGate) <= 2:
    print "No gate found"
else:
    print "Gate found" 

        # Find the index of the largest contour
areas = [cv2.contourArea(c) for c in contoursY]
areasDes = sorted(areas,reverse = True)
#i = 0

#max_index = np.argmax(areas)
cnt = contoursY[0]
cnt1 = contoursY[2]
cnt2 = contoursY[4]

contoursYnew.append(cnt)
contoursYnew.append(cnt1)
contoursYnew.append(cnt2)

        # Create Rectangle around largest contour (ROI)
x, y, w, h = cv2.boundingRect(cnt)
x1, y1, w1, h1 = cv2.boundingRect(cnt1)
x2, y2, w2, h2 = cv2.boundingRect(cnt2)


roi = YgateIm[y:y+h,x:x+w]
roi1 = YgateIm[y1:y1+h1,x1:x1+w1]
roi2 = YgateIm[y2:y2+h2,x2:x2+w2]

cv2.rectangle(YgateIm, (x, y), (x+w, y+h), (255, 0, 0), 2)
cv2.rectangle(YgateIm, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 2)
cv2.rectangle(YgateIm, (x2, y2), (x2+w2, y2+h2), (0, 0, 255), 2)
        
mask = np.zeros(roi.shape,np.uint8)
mask[y:y+h,x:x+w] = roi[y:y+h,x:x+w]
output = cv2.bitwise_and(roi, mask)

# # Filter for Max RGB values
#b, g, r = cv2.split(output)
#M = np.maximum(np.maximum(r, g), b)
#r[r < M] = 0
#g[g < M] = 0
#b[b < M] = 0
#
#        # Merge back into a maximum RGB image
#image2 = cv2.merge([b, g, r])
        
        
for i in xrange(len(contoursYnew)):
     #cv2.drawContours(YgateIm, contoursY,  -1, (255), 2)
     moments = cv2.moments(contoursYnew[i])
     centres.append((int(moments['m10']/moments['m00']),int(moments['m01']/moments['m00'])))
     c#v2.circle(YgateIm, centres[-1], 7, (0, 0, 255), -1)  
     #cv2.circle(YgateIm, centres[1], 7, (0, 0, 255), -1)
     #cv2.circle(YgateIm, centres[2], 7, (0, 0, 255), -1)
     cv2.circle(YgateIm, (305,183), 7, (34, 0, 100), -1)
     cv2.circle(YgateIm, (80,183), 7, (255, 255, 0), -1)
     cv2.circle(YgateIm, (530,183), 7, (0, 255, 0), -1)
     cv2.circle(YgateIm, (305,355), 7, (0, 0, 255), -1)

#if centres[0][0] > centres [1][0]:
    
     
        
cv2.imshow("Target",output)
cv2.imshow("cnts", YgateIm)
cv2.imshow("Edges",Ygate_edges)
cv2.imshow("Segmented Image",segmented_image )

cv2.waitKey(0)
cv2.destroyAllWindows () 