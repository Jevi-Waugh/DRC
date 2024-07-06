import cv2 as cv
def harris_corner_detection(self, binary_mask) -> int:
    frame = cv.cornerHarris()
    # return length of corners


def detect_7_corners(self):
    # get the Contour
    # use harris corner detection on the contour mask or photo
    # but find a way to accurately expect the arrow
    pass


def arrow_detect(self):
    # process frame and use a bianry mask such as black and white
    
    # get the contour of that mask
    
    
    # use harris corner detection on the contour mask
    
    
    # make sure that the center of the frame is in line with the center of the arrow
    # if not adjust
    
    
    # if there are pixel values to the left of the frame then it is a left arrow
    
    # else a right arrow