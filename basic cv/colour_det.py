import numpy as np
import cv2

# HSV range for blue
blue_lower = np.array([100, 150, 50])
blue_upper = np.array([140, 255, 255])

# HSV range for yellow
# Hard coded for now
yellow_lower = np.array([20, 100, 100])
yellow_upper = np.array([30, 255, 255])

def process_frame(frame):
    # Convert  frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks for blue and yellow
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Combine masks to get  full path
    combined_mask = cv2.bitwise_or(blue_mask, yellow_mask)

    return combined_mask, blue_mask, yellow_mask
