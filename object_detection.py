import cv2 as cv
import numpy as np
from droid import Droid
import time
def detect_purple_obstacle(droid: Droid, mask=None, contours=None) -> bool:
    # passing the droid object by reference.
    colour = (0, 100, 255)
    max_c = 0
    if mask is None:
        mask = droid.PURPLE_MASK
    purple_edges = droid.canny_edge(mask)
    # What if contour edges cannot be picked up
    if contours is None:
        contours = droid.find_contours(purple_edges)
        if contours:
            max_c = max(contours, key=cv.contourArea)
            # droid.purple_centroid = droid.get_centroid(max_c)
    i : int = 0
    if contours:
        for epsilon in np.linspace(0.001, 0.05, 10):
            # Bug HERE -> Fix on saturday
            print("Iteration:", i)
            print("Epsilon value:", epsilon)
            
            perimeter = cv.arcLength(max_c, closed=True)
            approx = cv.approxPolyDP(max_c, epsilon * perimeter, closed=True)
            o_image = mask.copy()
            # approximate box
            (x_axis_tl, y_axis_tl, width, height) = cv.boundingRect(max_c)
            droid.obstacle_area = width, height
            droid.purple_centroid = width//2, height//2
            cv.drawContours(o_image, [max_c], -1, colour, 3)
            result = "eps={:.4f}, points={}".format(epsilon, len(approx))
            cv.putText(o_image, result, (x_axis_tl, y_axis_tl-30), cv.FONT_HERSHEY_COMPLEX, 0.7, colour, 3)
            i += 1
            
            if len(approx) == 4 and droid.area_threshold < max_c:
                droid.obstacle = True  
                droid.test_obstacle_detection(i, result, o_image)
                return True
            
            elif len(approx) == 4:
                # Recursive function as a safety contingency just incase.
                # Convex hull ->The smallest convex polygon that can contain all the points of the original contour.
                # will make it easier to find the box if there's a visual struggle
                # not sure if contours/max_c should be passed in for perimeter
                peri = cv.arcLength(contours, closed=True)
                epsilon = 0.01 * peri
                approximation_func =cv.approxPolyDP(max_c, epsilon, closed=True)
                contours = cv.convexHull(approximation_func)
                # recurse through
                detect_purple_obstacle(contours=contours)
            else: return False
    else: return False
    
            
            
# testing object detection on purple img
img = "Images/purple_img.jpg"
img = cv.imread(img)