
import numpy as np
import cv2

#Video capture object. (0)-> number of camera device
camera = cv2.VideoCapture(0)
#Define video object. Second parameter is the video codec
#Third parameter is the FPS of the video and last one is the FrameSize
#For LifeCam 20fps
video = cv2.VideoWriter('video10.avi', -1,10, (640,480));

while True:
    frame,imag = camera.read()
    video.write(imag)
    cv2.imshow("webcam", imag)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
#cv2.destroyAllWindows()
video.release()
