import cv2 as cv
import numpy as np
from droid import Droid
from object_detection import detect_purple_obstacle

def main():
    counter = 0
    while counter != 1:
        droid = Droid(camera_index = 0)
        # keep updating droid status
        
        droid.rbg_2_hsv()()
        # what if cx was only calculated with one tape -> 1 bug here
        # create a recalibration function to find both tapes i guess.
        deviation = droid.distance_to_turn(droid.frame.shape[1], cx=droid.center_x)
        # 1. invoke thread
        # thread1 = cx, cy = droid.detect_track()
        
        # 2. invoke thread 
        # thread2 = droid.directional_capabilities(deviation)
        
        # 3. invoke thread 
        # thread3 = detect_purple_obstacle(droid)
        
        
        # 4. invoke thread here for arrow detection
        # thread4 = detect_arrow(droid)
        
        
        
        droid.close_camera()
        counter += 1
        
if __name__ == "__main__":
    main()