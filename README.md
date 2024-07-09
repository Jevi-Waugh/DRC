# Droid Racing Challenge 2024/2025
This project implements an autonomous droid designed to navigate through a track strictly using Computer Vision (Cam & Ultrasonic sensor). The system detects the environment and captures essential infomation that allows it to make critical and informed decisions. The droid will start and stop only when it sees a green and end line.

## Table of Contents
* Vision system
* Robotic control and Multiprocessing
* Features
* Requirements
* Installation
* Usage
* Code Overview
  * Track Detection
  * Obstacle and Arrow Detection
  * Droid Detection
  * Multi-Processing
  * Robotic Control
* Authors
* Contributing
* License


## Vision system
This project implements a system that creates a spatial environment detecting critical information such as the boundaries that it's allowed to be within, for e.g. the track consisting of two tape, (yellow and blue). The vision system also looks out for the other red droids, maintaining a safe distance, avoiding objects (purple box) and implementing the estimation of object distance based off Focal length of the camera. The vision system is also trained to detect arrows by using contour detection and Harris Corner Detection.

## Robotic control and Multiprocessing

## Features

## Requirements
* Python 3.x
* OpenCV 4.x
* Numpy
* RPi.GPIO
* POSIX for Message queues

## Installation
1. Clone this repo.
   git clone https://github.com/Jevi-Waugh/DRC.git
2. Make sure you have Numpy, OpenCV and Posix for python and C
   pip install numpy opencv-python
   pip install posix_ipc
3. Install RPi.GPIO for Raspberry Pi:
   sudo apt-get update
   sudo apt-get install python3-rpi.gpio

## Usage

## Code Overview



## Authors
Jevi-Waugh - Vision System
jamis0 - Robotic control and Multi-processing
