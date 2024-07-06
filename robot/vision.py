from sys import stdout, stderr
from posix_ipc import *
from time import sleep
import struct
import random
import sys

from droid import *

STDOUT_PREFIX = "visn: "
STDOUT_PREFIX = "visn: "

QUEUE_WRITE_NAME = "/DRC-CONT-DATA"
QUEUE_WRITE_SIZE = 64
SIGNITURE = 1

def main():
    writeQueue = open_queue_write(QUEUE_WRITE_NAME)
    print(STDOUT_PREFIX + f"Opened queue \"{QUEUE_WRITE_NAME}\"")
    stdout.flush()

    droid = Droid(camera_index = 0, droid_status=True)
    droid.deploy_rgb_2_hsv()
    
    while True:
        centroid = droid.detect_track()  
        
        
        
        message = write_message(centroid)
        writeQueue.send(message)
        print(STDOUT_PREFIX + f"Sent ({centroid[0]:>3}, {centroid[1]:>3})")
        stdout.flush()

        sleep(1)


def open_queue_write(qName):
    while True:
        try:
            return MessageQueue(
                qName,
                read = False,
                write = True)
        except ExistentialError:
            print(STDOUT_PREFIX + f"Failed to open queue \"{QUEUE_WRITE_NAME}\"")
            print(STDOUT_PREFIX + f"Retrying...")
            stdout.flush()
            sleep(0.2)


def write_message(c):
    iscent = False if c == (None, None) else True
    x = -1 if None else c[0]
    y = -1 if None else c[1]
    return struct.pack("iiii", SIGNITURE, iscent, x, y)

if (__name__ == "__main__"):
    main()