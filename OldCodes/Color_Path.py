# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 21:12:47 2017

@author: ernes
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

pathIm = cv2.imread('frame7.jpg')
cv2.imshow('Path Image', pathIm)

lower_thresh = np.array([0,0,90], dtype='uint8')
upper_thresh = np.array([40,130,255], dtype='uint8')
segmented_image = cv2.inRange(pathIm, lower_thresh, upper_thresh)
cv2.imshow('Segmented Image',segmented_image)



