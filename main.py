import cv2 as cv
import numpy as np
from droid import Droid
from object_detection import detect_purple_obstacle
import multiprocessing
from ipcqueue import posixmq
from MotorAPI import MotorAPI_Reciever
from VisionAPI import close_unlink_queue
from VisionAPI import VisionAPI_Sender


def main():
    counter = 0
    while counter != 1:
        # Vision to Motor
        V2M = posixmq.Queue('/DRC-Vision-Motor-data', maxmsgsize=1024)
        # Motor to Vision
        M2V = posixmq.Queue('/DRC-Motor-Vision-data', maxmsgsize=1024)
        
        # Create the sender and receiver processes
        VISION_API_PROCESS = multiprocessing.Process(target=VisionAPI_Sender)
        CONTROL_API_PROCESS = multiprocessing.Process(target=MotorAPI_Reciever)

        # Start the processes
        VISION_API_PROCESS.start()
        CONTROL_API_PROCESS.start()

        # Wait for the processes to finish
        VISION_API_PROCESS.join()
        CONTROL_API_PROCESS.join()
        
        V2M.close_unlink_queue()
        M2V.close_unlink_queue()
        print("Communication between processes has ended.")
        
   
        # 1. invoke thread
        # thread1 = cx, cy = droid.detect_track()
        # deviation = droid.distance_to_turn(droid.frame.shape[1], cx=droid.center_x)
        
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
    
    
