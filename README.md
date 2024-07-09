# Droid Racing Challenge 2024/2025
This project implements an autonomous droid designed to navigate through a track strictly using Computer Vision (Cam & Ultrasonic sensor). The system detects the environment and captures essential infomation that allows it to make critical and informed decisions. The droid will start and stop only when it sees a green and end line.

## Table of Contents
* Introduction
*Features
*Requirements
*Installation
*Usage
*Code Overview
*Arrow Detection
*Droid Navigation
*Obstacle Avoidance
*Authors
*Contributing
*License


## Vision and Spatial Environment detection system
This project implements a system that creates a spatial environment detecting critical information such as the boundaries that it's allowed to be within, for e.g. the track consisting of two tape, (yellow and blue). The vision system also looks out for the other red droids, maintaining a safe distance, avoiding objects (purple box) and implementing the estimation of object distance based off Focal length of the camera. The vision system is also trained to detect arrows by using contour detection and Harris Corner Detection.


## Robotic control and Multiprocessing

Table of Contents
