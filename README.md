# Droid Racing Challenge 2024/2025

Arrow Detection and Navigation System
This project implements a system to detect arrows on a track and navigate accordingly. The system uses computer vision techniques to identify and respond to black arrows on white sheets, placed on a black ground.

Table of Contents
Introduction
Features
Requirements
Installation
Usage
Code Overview
Contributing
License
Introduction
This project aims to create a robust arrow detection and navigation system for a robotic vehicle. The system uses OpenCV for image processing and detection, ensuring that the robot can follow directional arrows placed on a track.

Features
Preprocessing: Converts frames to grayscale and applies Gaussian blur.
Thresholding: Uses adaptive thresholding to create binary images.
Edge Detection: Utilizes Canny edge detection to find edges.
Morphological Operations: Cleans up edges with morphological operations.
Contour Detection: Detects and approximates contours to polygons.
Corner Detection: Uses Harris corner detection to identify arrow shapes.
Arrow Validation and Direction Detection: Validates arrow shapes and determines their direction.
Requirements
Python 3.x
OpenCV 4.x
Numpy
Installation
Clone the repository:
