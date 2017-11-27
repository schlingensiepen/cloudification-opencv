#!/usr/bin/env python
#
# Text script for OpenCV-python script
#
# Script opens a camera as video source and starts
# reading frames and display then in a window called 'cam'
#
# This sample script is part of the cource cloudification.
# 


import time
import tempfile
import os

import numpy as np
import cv2

timeout = 200
chainlength = 5
start = time.monotonic() * 1000
lowerbound = 5000
upperbound = 10000
moving = False

framechain = []
# Generate video source by opening first source of system
cap = cv2.VideoCapture(0)
tmpFolder = tempfile.mkdtemp();
tmpFileCounter = 0

print ("Tempfolder for this session is " + tmpFolder)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Check for initialisation error
    if not ret:
        print ("Init error")
        quit()
    # Display the resulting frame
    cv2.imshow('cam',frame)

    step1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('step1',step1)

    step2 = cv2.GaussianBlur(step1, (21, 21), 0)
    cv2.imshow('step2',step2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if (time.monotonic()*1000 - start) < timeout :
        continue
    start = time.monotonic()*1000
    framechain.append(step2)
    if len(framechain) < chainlength:
        print ("\a")
        continue

    oldframe = framechain.pop(0)
    cv2.imshow('oldframe',oldframe)
    frameDelta = cv2.absdiff(oldframe, step2)
    cv2.imshow('frameDelta',frameDelta)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('thresh',thresh)

    dilated = cv2.dilate(thresh, None, iterations=2)
    cv2.imshow('dilated',dilated)

    (_, cnts, _) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    frame2 = frame.copy()
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 20:
            continue
 
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('cam2',frame2)
    count = cv2.countNonZero(thresh);

    if moving :
        if (count < lowerbound):
            moving = False
            filename = str(tmpFileCounter)
            filename.rjust(8,'0')
            filename = filename + ".png"
            print (filename + "\a")
            filename = os.path.join (tmpFolder, filename)
            tmpFileCounter+=1
            cv2.imwrite(filename,frame)
    else:
        if (count > upperbound):
            moving = True

# Release video source
cap.release()
cv2.destroyAllWindows()