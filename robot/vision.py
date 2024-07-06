from droid import *
from object_detection import detect_purple_obstacle
from sys import stdout, stderr
from posix_ipc import *
from time import sleep
import struct
import random
import sys

STDOUT_PREFIX = "visn: "
STDOUT_PREFIX = "visn: "

QUEUE_WRITE_NAME = "/DRC-CONT-DATA"
QUEUE_WRITE_SIZE = 64
SIGNITURE = 1

X_MIN = 0
X_MAX = 400

Y_MIN = 0
Y_MAX = 200


def main():
    writeQueue = open_queue_write(QUEUE_WRITE_NAME)
    print(STDOUT_PREFIX + f"Opened queue \"{QUEUE_WRITE_NAME}\"")
    stdout.flush()

    droid = Droid(camera_index = 0, droid_status=True)
    droid.deploy_rgb_2_hsv()
    while True:
        x, y = droid.detect_track()
        deviation = droid.distance_to_turn(droid.frame.shape[1], cX=droid.center_x)
        obstacle = detect_purple_obstacle(droid)

        if (x == None or y == None):
            continue
        
        message = write_message(x, y)
        writeQueue.send(message)

        print(STDOUT_PREFIX + f"Sent ({x:>3}, {y:>3})")
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


def write_message(x, y):
    return struct.pack("iii", SIGNITURE, x, y, obstacle, arrow)

if (__name__ == "__main__"):
    main()
