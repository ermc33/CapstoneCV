#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#"""
#Created on Mon Apr  3 11:41:37 2017
#
#@author: Edwin
#"""

import cv2
import numpy as np
import math
import glob 
#import AngleTest 
#"""""""""""""""""""""""""""""""""Classifier"""""""""""""""""""""""""""""""""
def MED(x,y):
    for i in range(len(miu)):
        ListVec = [] 
        vecx1 = x[0] - miu[i]
        ListVec.append(vecx1)
        vecx2 = x[1] - miu[i]
        ListVec.append(vecx2)
        vecx3 = x[2] - miu[i]
        ListVec.append(vecx3)
        ListVec = np.asarray(ListVec) #convert list to array
        ListVecTrans = np.transpose(ListVec)
        mult1 = ListVecTrans[0]*ListVecTrans[0]
        mult2 = ListVecTrans[1]*ListVecTrans[1]
        mult3 = ListVecTrans[2]*ListVecTrans[2]
        dist = mult1 + mult2 + mult3
        dist = math.sqrt(dist)
        Distance.append(dist)

    return Distance  
#"""""""""""""""""""""""""""""Distance Calculation"""""""""""""""""""""""""
def distance_Calc(real_width, focal_length, perc_width):
    distance = (real_width * focal_length)/perc_width
    return distance
#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

#Variables definition
IdealThresh= np.array([135, 119, 86], dtype = 'uint8')
contours = np.array([])
cont = np.array([])
hierarchy = np.array([])
centres = []
CropCoord = []
contour_List = []
miu = []
Distance = []
Circle_List = []
circles = []
kernel = np.ones((3,3), np.uint8)
drawing = np.zeros([400, 630],np.uint8)
idx = 0
count = 10
MaxNumObjects = 3
focal_length = 833.999 #calibration parameter
real_width = 7.01   #buoy width 

#Original Image and its resizing
img = cv2.imread("omar7.jpg")
img2 = img.copy()
img = cv2.resize(img,(630,400))
img2 = cv2.resize(img2,(630,400))

#Original image is filtered, then the canny edge operator is applied
FilteredImage = cv2.bilateralFilter(img,3,500,500)
edges = cv2.Canny(FilteredImage, 0,100, True)

#Using the edge map, the contours in the image are calculated                            
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, contours, hierarchy)

#Selecting contours based on area and number of vertices                        
for contour in contours :
    approxC = cv2.approxPolyDP(contour, 0.02*cv2.arcLength(contour,True),True)
    areaC= cv2.contourArea(contour)
    if len(approxC) >= 5  and areaC >10:
         contour_List.append(contour)
         
#Drawing selected contours in a new black image    
for i in xrange(len(contour_List)):
    cv2.drawContours(drawing, contour_List,  -1, (255), 2)
    moments = cv2.moments(contour_List[i])
    centres.append((int(moments['m10']/moments['m00']),int(moments['m01']/moments['m00'])))
    cv2.circle(drawing, centres[-1], 7, (255, 255, 255), -1)
    
drawing_erode = cv2.erode(drawing, kernel, iterations=1)
drawing_erode = cv2.bitwise_not(drawing_erode)

#"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""" 
#Changing contour image to grayscale
cv2.imwrite('ContourImage.jpg', drawing)
circles_image = cv2.imread('ContourImage.jpg')
circles_image = cv2.cvtColor(circles_image,cv2.COLOR_BGR2GRAY)

#Resizing image with circles to same dimensions as original
height, width = img.shape[:2]
circles_image = cv2.resize(circles_image, (width, height))

#Obtain contours of circles image and create bounding boxes for each of the 
#the objects in the image. According to the dimensions of the box, crop the
#object. Save in CropCoord the coordinates in the original image of those images
#that were cropped.  
contours, _ = cv2.findContours(circles_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for c in contours:
    x, y ,w, h = cv2.boundingRect(c)
    if w>30 and h>30:
        idx+=1
        crop_image = img[y:y+h,x:x+w]
        CropCoord.append([x,y,w,h])
        cv2.imwrite("file%i.jpg"%idx, crop_image)

#Access each of those cropped images and calculate its mean. Save the mean of
#each image in miu.        
for name in glob.glob('C:\Users\ernes\.spyder/file?.jpg'):
    print name
    circle = cv2.imread(name)
    M = np.mean(circle)
    miu.append(M) 

#Execute classifier and get the index of the buoy"    
MED(IdealThresh,miu)
Min_Distance = min(Distance)  
index = Distance.index(Min_Distance)  

#Trace that index to CropCoord[] to obtain the classified circular object (buoy)
Buoy = CropCoord[index]

#Draw a rectangle with the bounding box dimensions and coordinates on the 
#original image
x = Buoy[0]
y = Buoy[1]
w = Buoy[2]
h = Buoy[3]
cv2.rectangle(img2, (x,y),(x+w,y+h),(0,255,0),3)
cv2.imshow('Classified Image', img2)

#Calculate center of bounding rectangle
centerx = x + x+w
centerx = centerx/2
centery = y + y+h
centery = centery/2
RectCenter = (centerx, centery)
#print RectCenter

#Create a new image with the cropped buoy 
buoy_crop = img[y:y+h, x:x+w]
mask = np.zeros((height, width,3),np.uint8)
mask[y:y+h, x:x+w] = buoy_crop
mask = cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)

#Calculate Hough Circles Transform in the cropped classified image
circles = cv2.HoughCircles(mask,cv2.cv.CV_HOUGH_GRADIENT,2,1,
                           param1=50,param2=50,minRadius=0,maxRadius=75)

#Check if the classified object is a circle or not
if circles == None:
    buoy_found = False
else:
    buoy_found = True
    
print "buoy_found = ", buoy_found   

for i in circles[0,:]:
     cv2.circle(mask,(i[0],i[1]),i[2],(0,255,0),2)  #draw the outer circle
     cv2.circle(mask,(i[0],i[1]),2,(0,0,255),3)     #draw the center of the circle
     
cv2.imshow('Hu circle', mask)

###############################################################################
#Test if the classified circular object is actually the desired color
(b,g,r) = cv2.split(buoy_crop)

average_color_per_row = np.average(b, axis=0)   #average value of each row
average_color = np.average(average_color_per_row, axis=0)  #average of average
average_color = np.uint8(average_color)   #convert to uint8 (0-255)  

average_color_per_row2 = np.average(g, axis=0)   #average value of each row
average_color2 = np.average(average_color_per_row2, axis=0)  #average of average
average_color2 = np.uint8(average_color2)   #convert to uint8 (0-255) 


average_color_per_row3 = np.average(r, axis=0)   #average value of each row
average_color3 = np.average(average_color_per_row3, axis=0)  #average of average
average_color3 = np.uint8(average_color3)   #convert to uint8 (0-255) 
 
avg_bgr = [average_color, average_color2, average_color3]
print avg_bgr

#Find edges and contours in cropped image
edgeCrop = cv2.Canny(buoy_crop, 0,100, True)
#cv2.imshow('Edges of Crop', edgeCrop)

cont, g = cv2.findContours(edgeCrop, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Find the biggest contour in image and draw a circle using the biggest contour
#in the cropped image
c = max(cont, key = cv2.contourArea)       
circ = cv2.minEnclosingCircle(c)
cv2.circle(buoy_crop, (int(circ[0][0]),int(circ[0][1])), int(circ[1]), (255,100,0), 3)

#Calculate radius and diameter of drawn circle
radius = circ[1]
diameter = radius * 2

#Calculate the distance of the buoy using the diameter and print it
distance = distance_Calc(real_width, focal_length, diameter)
dist_ft = distance/12
print dist_ft

cv2.imshow('Original Image', img)
#cv2.imshow("CROP",crop_buoy)    
cv2.imshow ("New Image", drawing)   
cv2.imshow("edges",edges)

#AngleTest.centerBuoyX(RectCenter[0])
#AngleTest.centerBuoyY(RectCenter[1])
