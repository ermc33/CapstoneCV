#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:04:33 2017

@author: Edwin
"""
"""This code is meant to be used as a frame grabber. Everytime the function is
called a frame is stored, in the variable named image, to be analized. """
import cv2
import numpy as np
#count = 0 
def Frame_Grab ():
    global count
    global image
    cap = cv2.VideoCapture(0)
    success,image = cap.read()
    #count = 0
    #success = True    
    if success== True:
        success,image = cap.read()
        print 'Read a new frame: ', success
        cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
        
        count += 1
        #if count == 1 :
        cap.release()
        print success
        print count
      
    elif success == False:
        print "No Image"
        print success
        
       
    return (image, success)
    

Frame_Grab()  
cv2.destroyAllWindows()