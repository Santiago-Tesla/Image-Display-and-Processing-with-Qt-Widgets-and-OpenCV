# Image-Display-and-Processing-with-Qt-Widgets-and-OpenCV
This Python code implements a simple video processing application with a graphical user interface (GUI) using PyQt5. It allows users to capture video from a webcam and apply various image processing effects in real-time.

## Features:

Start/stop video capture from the default camera (camera ID 0).
Apply the following image processing effects (only one can be active at a time):
Edge detection using Canny edge detection.
Grayscale thresholding with a user-adjustable threshold.
Face detection using a Haar cascade classifier.
Eye detection using a Haar cascade classifier (requires a face detection model).

## How to Use:

Run the script: python video_processor.py
Click the "Start Camera" button to start capturing video.
Use the following buttons to enable/disable image processing effects:
Edge Detection
Grayscale with Threshold
Face Detection
Eye Detection
Adjust the threshold slider (only applicable for grayscale thresholding) to change the threshold value.
Click the "Save Frame" button to save the current frame as an image file.
Click the "Exit" button to close the application.

## Requirements:

Python 3.x
OpenCV library (pip install opencv-python)
PyQt5 library (pip install PyQt5)
