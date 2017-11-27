#!/usr/bin/env python
#
# Text script for OpenCV-python script
#
# Script opens a camera as video source and starts
# reading frames and display then in a window called 'cam'
#
# This sample script is part of the cource cloudification.
# 


import numpy as np
import cv2

# Generate video source by opening first source of system
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Check for initialisation error
    if not ret:
        print ("Init error")
        quit()

    # Display the resulting frame
    cv2.imshow('cam',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video source
cap.release()
cv2.destroyAllWindows()