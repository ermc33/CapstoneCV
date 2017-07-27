#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 21:10:18 2017

@author: Edwin
"""

import cv2
vidcap = cv2.VideoCapture('videoLifeCamSteady1.mov')
success,image = vidcap.read()
count = 0
GrabFrame_true = True
while success:
  GrabFrame,image = vidcap.read()
  print('Grabate ESTE: ', GrabFrame_true)
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  count +=1
  if count == 20 :#Control variable. Change it depending on how many images you want 
      success = False 
