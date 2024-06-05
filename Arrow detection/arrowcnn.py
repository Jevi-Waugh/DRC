import cv2
# from torch.nn import Module
from torch.nn import Conv2d
from torch.nn import Linear
from torch.nn import MaxPool2d
from torch.nn import ReLU
from torch.nn import LogSoftmax
from torch import flatten

import math
import numpy

class ArrowCnn():
    def __init__(self):
        # use tranfer learning so that the model learns faster
        # resolution depends but we def need pooling for arrows
        pass
        
    def detect_trail(self, frame,camera_index) -> list:
        """return coordinates to determine how many degrees we will be rotating or going towards"""
        # detect if there is a line and compare previous line to detect the derivative which will help 
        # navigating the robot
        # use guassian blur and canny edge
        
        cap = cv2.VideoCapture(camera_index)  # Open the specified camera
        if not cap.isOpened():
            print("Error: Could not open video stream")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 1.5)
            edges = cv2.Canny(blur, 50, 150)
            lines = cv2.HoughLinesP(edges, 1, cv2.pi/180, 50, minLineLength=50, maxLineGap=10)

            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

            cv2.imshow('Droid Line Following', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()