import cv2 as cv
from ipcqueue import posixmq
from motor import motor
def MotorAPI(send_q, recieve_q):
    deviation = recieve_q.get()
    # find a way to get the deviation
    # because getting this data could give either the arrow result
    # or the obstacle boolean result.
    # assume this is correct for now.
    motor_dummy = motor()
    if motor_dummy.green_line[0]== 1:
        # this prolly has to be in a
        motor_dummy.directional_capabilities(deviation)
        motor_dummy.green_line == False
        
    else:
        # put
        Exception("Crtitcal Error, cannot find start line")
    
    messages = []
    
    # send message.