import cv2 as cv
from ipcqueue import posixmq

def MotorAPI_Reciever():
    queue = posixmq.Queue('/test_queue')

    while True:
        msg = queue.get()
        if msg == 'END':
            break
        print(f'Received: {msg}')
        