import cv2 as cv
import numpy as np
from droid import Droid
from object_detection import detect_purple_obstacle
import multiprocessing
from ipcqueue import posixmq
from MotorAPI import MotorAPI
from VisionAPI import close_unlink_queue
from VisionAPI import VisionAPI

# CRUCIAL COMMENT!!!

def main():
    # PIPELINE
    counter = 0
    while counter != 1:
        # Vision to Motor
        V2M = posixmq.Queue('/DRC-Vision-Motor-data', maxmsgsize=1024)
        # Motor to Vision
        M2V = posixmq.Queue('/DRC-Motor-Vision-data', maxmsgsize=1024)
        
        # create processes and have both queues as arguments
        VISION_API_PROCESS = multiprocessing.Process(target=VisionAPI, args=(V2M,M2V))
        CONTROL_API_PROCESS = multiprocessing.Process(target=MotorAPI, args=(M2V,V2M))
    

        # Start both processes
        VISION_API_PROCESS.start()
        CONTROL_API_PROCESS.start()

        # Wait for the processes to finish
        VISION_API_PROCESS.join()
        CONTROL_API_PROCESS.join()
        
        # V2M.close_unlink_queue()
        # M2V.close_unlink_queue()
        
        print("Communication between processes has ended.")
    
        # droid.close_camera()
        counter += 1
        
if __name__ == "__main__":
    main()
    
    
