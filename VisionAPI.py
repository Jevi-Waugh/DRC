import time
# from ipcqueue import posixmq
from droid import Droid
from object_detection import detect_purple_obstacle

def VisionAPI(send_q=None, recieve_q=None):
    """This will have the vision Process and will send input and recive output
    Not sure if this will be the final structure for the spatial analysis and activity
    but Multithreading is strongly on the table"""
    
    # setting up the vision control for the droid
    # this might be done in main if process can handle enough byte for the Droid object
    droid = Droid(camera_index = 0)
    droid.rbg_2_hsv()
    cx, cy = droid.detect_track()
    # droid.center_x = 320
    deviation = droid.distance_to_turn(droid.frame.shape[1], cX=droid.center_x)
    obstacle = detect_purple_obstacle(droid)
    print(f"deviaton={deviation}, obstacle={obstacle}")
    # detect arrow here
    
    # setting up queue
    # maybe typecast multiple data into a string for easy send off messages

    messages = []
    
    # send message.

def close_unlink_queue(queue):
    queue.close()
    queue.unlink()
    

VisionAPI()