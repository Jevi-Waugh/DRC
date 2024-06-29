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
    motor_dummy.directional_capabilities(deviation)
    
    messages = []
    
    # send message.