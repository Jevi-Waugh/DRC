import cv2 as cv
import numpy as np
from droid import Droid

def main():
    counter = 0
    while counter != 1:
        droid = Droid(camera_index = 0)
        # keep updating droid status
        droid.detect_track()
        droid.close()
        counter += 1
        
if __name__ == "__main__":
    main()