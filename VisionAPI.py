import time
# from ipcqueue import posixmq
from droid import Droid
from object_detection import detect_purple_obstacle

def VisionAPI(send_q=None, recieve_q=None):
    # testing branch
    """This will have the vision Process and will send input and recive output
    Not sure if this will be the final structure for the spatial analysis and activity
    but Multithreading is strongly on the table"""
    
    # setting up the vision control for the droid
    # this might be done in main if process can handle enough byte for the Droid object
    droid = Droid(camera_index = 0, droid_status=True)
    droid.deploy_rgb_2_hsv()
    # below is to repeat
    # Detect green line first.
   
    # if green line is detected, then GO!
    cx, cy = droid.detect_track()
    droid.green_line = True if not droid.green_contours else False
    # droid.center_x = 320
    deviation = droid.distance_to_turn(droid.frame.shape[1], cX=droid.center_x)
    obstacle = detect_purple_obstacle(droid)
    print(f"deviaton={deviation}, obstacle={obstacle}")
    print(droid.__repr__())
            
            
            # Finish line
             
            
            # By the time this statement is reacged the droid would have probably gone off the 
            # green start line unable to pick it uop again restting its value therefore this is feasable
    
    # Need to put data
    # detect arrow here
    
    # also detect other droid.
    
    # setting up queue
    # maybe typecast multiple data into a string for easy send off messages

    messages = []
    
    # send message.

def close_unlink_queue(queue):
    queue.close()
    queue.unlink()
    

# Currently running this file for testing andf debugging
VisionAPI()