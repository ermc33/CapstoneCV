# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:00:35 2017

@author: ernes
"""
import cv2
import numpy as np

output_image = np.array([])

#Image
#image = cv2.imread('Boyas.jpg')
#gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#OrgRez = cv2.resize(image, (500,300))
#cv2.imshow("Image", OrgRez)


crop = cv2.imread('file5.jpg')
(b,g,r) = cv2.split(crop)
cv2.imshow('crop', crop)
#(b2,g2,r2) = cv2.split(crop_image2)


average_color_per_row = np.average(b, axis=0)   #average value of each row
average_color = np.average(average_color_per_row, axis=0)  #average of average
average_color = np.uint8(average_color)   #convert to uint8 (0-255) 
#average_color_img = np.array([[average_color]*100]*100, np.uint8)
#cv2.imshow('avg',average_color_img)  

average_color_per_row2 = np.average(g, axis=0)   #average value of each row
average_color2 = np.average(average_color_per_row2, axis=0)  #average of average
average_color2 = np.uint8(average_color2)   #convert to uint8 (0-255) 


average_color_per_row3 = np.average(r, axis=0)   #average value of each row
average_color3 = np.average(average_color_per_row3, axis=0)  #average of average
average_color3 = np.uint8(average_color3)   #convert to uint8 (0-255) 
 
avg_bgr = [average_color, average_color2, average_color3]
print avg_bgr

#black = np.array([0,0,0], dtype='uint8')
#thresh = np.array([average_color,average_color2,average_color3], dtype='uint8')
#output_image = cv2.inRange(image, black, thresh)
#cv2.imshow('red',output_image)
