
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:24:37 2017

@author: Edwin
"""
import cv2
import numpy as np
import messPassing
#Libreria para visualizar
#import matplotlib.pyplot as plt
#import AngleTest 

#Start Searching path and angle
def startPathPCA():
    message = messPassing.messPassing()
    contours = np.array([])
    hierarchy = np.array([])
    contour_List1 = [] 
    k = 0
    ID =0
    count =0
    
    pathIm = cv2.imread("camTest0.jpg")
    pathIm = cv2.resize(pathIm, (630,400))
    pathIm2 = pathIm.copy()
    Filt_path = cv2.bilateralFilter(pathIm,7,900,900)
     
    'Color Thresholds'
    lower_thresh = np.array([0,30,30], dtype='uint8') #Parameter to adjust in the pool
    upper_thresh = np.array([50,170,255], dtype='uint8')#Parameter to adjust in the pool
    'Image Segmentation'
    segmented_image = cv2.inRange(pathIm , lower_thresh, upper_thresh) 
    'Calculate Edge Map'
    path_edges = cv2.Canny(segmented_image, 0,100, True)
    'Find Contours'
    contours, hierarchy = cv2.findContours(path_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, contours, hierarchy)
    'Check if contours were found'
    if len(contours) ==0:
        print "Adjust canny"
    'Look for a rectangle'
    for contour in contours:
        approxV = cv2.approxPolyDP(contour, 0.02*cv2.arcLength(contour,True),True)
        if (( 4 <= len(approxV) <= 10)) :
            contour_List1.append(contour)
    'Check if rectangle were found'        
    if len(contour_List1) == 0:
        print "No rectangle found" 
       
    if not len(contour_List1) == 0:
        for cnt in contour_List1:
            count +=1
            kcomp = len(cnt)
            if kcomp > k:
                k = kcomp
                ID = count - 1             
            else: 
                k = k
    
    y_coor, x_coor = np.nonzero(path_edges)
    x_coor = x_coor - np.mean(x_coor) #Substracting x - xmean for stability 
    y_coor = y_coor - np.mean(y_coor)#Substracting y - ymean for stability 
    
    coords = np.vstack([x_coor, y_coor]) 
    cov = np.cov(coords) #Covariance Matrix
    evals, evecs = np.linalg.eig(cov) #EigenValues and EigenVectors
    sort_indices = np.argsort(evals)[::-1] #Sort EigenValues in decreasing order
    evec1, evec2 = evecs[:, sort_indices]
    x_v1, y_v1 = evec1  # Eigenvector with largest eigenvalue
    x_v2, y_v2 = evec2
    theta = np.tanh((x_v1)/(y_v1))
    theta = theta*100 #Angle for control system 
    message.angle(theta)
    #AngleTest.receive(theta)  #Angle for control system 
    #return value after calculating the angle
    return message

