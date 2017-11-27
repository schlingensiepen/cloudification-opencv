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
import argparse

import numpy as np
import cv2
start = time.monotonic() * 1000
moving = False


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", 
    help="path to the video file")
ap.add_argument("-t", "--timeout", type=int, default=100, 
    help="time out")
ap.add_argument("-c", "--chainlength", type=int, default=5, 
    help="threshold for still image")
ap.add_argument("-l", "--lowerbound", type=int, default=5000, 
    help="threshold for still image")
ap.add_argument("-u", "--upperbound", type=int, default=10000, 
    help="threshold for action image")

args = None
try:
    args = vars(ap.parse_args())
except:
    parser.print_help()
    sys.exit(0)

timed = False
if args.get("video", None) is None:
    cap = cv2.VideoCapture(0)
    time.sleep(0.25)
    timed = True
# otherwise, we are reading from a video file
else:
    cap = cv2.VideoCapture(args["video"])
    timed = False

timeout = args["timeout"]
chainlength = args["chainlength"]
lowerbound = args["lowerbound"]
upperbound = args["upperbound"]

print ("Starting with timeout ......: ", timeout)
print ("Starting with chainlength ..: ", chainlength)
print ("Starting with lowerbound: ..: ", lowerbound)
print ("Starting with upperbound: ..: ", upperbound)


framechain = []
# Generate video source by opening first source of system
# cap = cv2.VideoCapture(0)
tmpFolder = tempfile.mkdtemp();
tmpFileCounter = 0

print ("Tempfolder for this session is " + tmpFolder)
os.startfile(tmpFolder)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Check for initialisation error
    if not ret:
        print ("Init error")
        break
    # Display the resulting frame
    cv2.imshow('cam',frame)

    step1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('step1',step1)

    step2 = cv2.GaussianBlur(step1, (21, 21), 0)
    cv2.imshow('step2',step2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    if timed :
        if (time.monotonic()*1000 - start) < timeout :
            continue
    else:
        for i in range (0, round (25 * (timeout / 1000))):
            cap.read()
    start = time.monotonic()*1000
    framechain.append(step2)
    if len(framechain) < chainlength:
        print('.\a', end='', flush=True)
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
            tag = filename = filename.rjust(8,'0')
            cv2.imshow(filename,frame)
            filename = filename + ".png"
            print (filename + "\a")
            filename = os.path.join (tmpFolder, filename)
            tmpFileCounter+=1
            cv2.imwrite(filename,frame)

            # using findContours func to find the none-zero pieces
            #(_,cnts, hierarchy) = cv2.findContours(
            #    step1.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
            ret,thresh = cv2.threshold(step1,127,255,0)
            _ , cnts,hierarchy = cv2.findContours(thresh, 1, 2)

            chunkCounter = 0
            frame3 = frame.copy()
            for c in cnts:
                size = cv2.contourArea(c)
                if size >1000 and size < 5000:
                    (x, y, w, h) = cv2.boundingRect(c)
                    chunkfilename = os.path.join(
                        tmpFolder, tag + "-" + str(chunkCounter).rjust(4,'0') + ".png")
                    cv2.rectangle(frame3, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    roi = frame[y:y+h, x:x+w]
                    target_h = h
                    if target_h < 50 : target_h = 50
                    target_w = w
                    if target_w < 50 : target_w = 50
                    target_img = np.zeros((target_h,target_w,3), np.uint8)
                    target_img[:roi.shape[0], :roi.shape[1]]=roi
                    cv2.imwrite(chunkfilename, target_img)
                    chunkCounter+=1
            cv2.imshow(tag + " areas",frame3)
    else:
        if (count > upperbound):
            moving = True

if not timed:
    while (True):
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release video source
cap.release()
cv2.destroyAllWindows()