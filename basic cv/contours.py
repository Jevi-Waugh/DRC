import cv2 as cv

def find_contours(mask):
    # cv2.RETR_EXTERNAL will focus on the outer shape of the track
    # for Contour Approximation Method
    # maybe use simple for now to save memory, but later on prototyping
    # we might need to approximate for more boundary points 
    # although a little computationally expensive for the raspberry pi
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # offset irrelevant for now
    # Optional offset by which every contour point is shifted. 
    # This is useful if the contours are extracted from the image ROI and then they should be analyzed in the whole image context
    return contours

def get_centroid(contour):
    # moments will have area, centroid, and orientation of the pixel.
    # M will return a few moments in a dict format
    M = cv.moments(contour)
    # print(type(M["m10"]))
    vector = ()
    # The zeroth moment, which represents the area of the contour.
    if M["m00"] != 0:
        # Typecasting is crucial as the moments are in default float.
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    return cX, cY

def calculate_center_line(blue_contours, yellow_contours):
    if blue_contours and yellow_contours:
        blue_c = max(blue_contours, key=cv.contourArea)
        yellow_c = max(yellow_contours, key=cv.contourArea)
        
        # get centroids and return these coordinates as a tuple
        blue_centroid = get_centroid(blue_c)
        yellow_centroid = get_centroid(yellow_c)
        # print(type(yellow_centroid))

        # get middle of the line.
        center_x = (blue_centroid[0] + yellow_centroid[0]) // 2
        center_y = (blue_centroid[1] + yellow_centroid[1]) // 2

        return center_x, center_y
    return None, None
