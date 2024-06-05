# Obstacle detection
import numpy as np
import cv2 as cv

def obstacle_detection(self):
    # use feedback optimisation and control sound for any skew data
    # purple box
    # detect box and edges
    # create a purple array of hsv
    # hue - wavelength
    # saturation - brilliance and intensity
    # value - lightness/darkness
    purple_lower = [0,0,0]
    purple_upper = [0,0,0]
    red = np.uint8([[[0,0,255 ]]])  
    redHSV = cv.cvtColor(red, cv.COLOR_BGR2HSV) 
    print(redHSV) 
    pass

red = np.uint8([[[0,0,255 ]]])  
redHSV = cv.cvtColor(red, cv.COLOR_BGR2HSV) 
print(redHSV) 
