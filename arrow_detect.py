import cv2 as cv
from droid import Vision
def harris_corner_detection(self, binary_mask) -> list:
    pass
    # det(M)=λ1λ2
    # trace(M)=λ1+λ2
    # λ1 and λ2 are the eigenvalues of M\
    # R=det(M)−k(trace(M))2
    # return corners


def arrow_detect(self, vision_sys: Vision, frame) -> bool:
    # process frame and use a bianry mask such as black and white
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    processed_frame = cv.GaussianBlur(gray_frame, (5, 5), 0)
    # get the contour of that mask
    # BUG
    # Issue is that i might feed it white sheet to detect the arrow
    # but the contour itself will be the sheet and not the arrow.
    # i guess once i find 4 corners of the white sheet then get the frame inside that and get the contour again 
    # then expect 7 corners.
    contour = vision_sys.find_contours(processed_frame)
    corners = harris_corner_detection(contour)
    
    # use harris corner detection on the contour mask
    if len(corners) == 7:
        vision_sys.arrow = True
        # center the frame.
        # frame[y, x]
        # frame[start_row:end_row, start_col:end_col]
        height, width, _ = frame.shape
        left_frame = frame[:, :width]
        # right_frame = frame[:, width:]
        contour_lf = vision_sys.find_contours(left_frame)
        # contour_rf = vision_sys.find_contours(right_frame)
        # computationally expensive but need to check if we are correct.
        vision_sys.arrow_dir = "left" if len(contour_lf) == 5 else "right"
            
    # make sure that the center of the frame is in line with the center of the arrow
    # if not adjust
    
    
    # if there are pixel values to the left of the frame then it is a left arrow
    
    # else a right arrow
    return vision_sys.arrow