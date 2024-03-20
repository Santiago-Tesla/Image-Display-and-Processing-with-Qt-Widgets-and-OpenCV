# Image-Display-and-Processing-with-Qt-Widgets-and-OpenCV
This Python code implements a simple video processing application with a graphical user interface (GUI) using PyQt5. It allows users to capture video from a webcam and apply various image processing effects in real-time.

## Features:

1. Start/stop video capture from the default camera (camera ID 0).
2. Apply the following image processing effects (only one can be active at a time):
   
   i) Edge detection using Canny edge detection.
   
   ii) Grayscale thresholding with a user-adjustable threshold.
   
   iii) Face detection using a Haar cascade classifier.
   
   iv) Eye detection using a Haar cascade classifier (requires a face detection model).

## How to Use:

1. Run the script: python video_processor.py
2. Click the "Start Camera" button to start capturing video.
3. Use the following buttons to enable/disable image processing effects:
   
   i) Edge Detection
   
   ii) Grayscale with Threshold
   
   iii) Face Detection
   
   iv) Eye Detection
   
5. Adjust the threshold slider (only applicable for grayscale thresholding) to change the threshold value.
6. Click the "Save Frame" button to save the current frame as an image file.
7. Click the "Exit" button to close the application.

## Requirements:

1. Python 3.x
2. OpenCV library (pip install opencv-python)
3. PyQt5 library (pip install PyQt5)
