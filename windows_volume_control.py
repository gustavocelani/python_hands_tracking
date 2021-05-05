
# Imports
import cv2 as cv
import time
import numpy as np
import hand_track_module as htm # Local Library
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# FPS Calcule Control
pTime = 0

# WebCam Setup
wCam, hCam = 640, 480
capture = cv.VideoCapture(0)
capture.set(3, wCam)
capture.set(4, hCam)

# WebCam Validation
if not capture.isOpened():
    print('[FATAL ERROR] Fail to open WebCam')
    exit()

# Initializing Hands Detector
detector = htm.HandsDetector(detecConf=0.7)

# Windows Speakers Setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
systemVolume = cast(interface, POINTER(IAudioEndpointVolume))

# Getting Volume Range
systemVolumeRange = systemVolume.GetVolumeRange()
systemVolumeMin = systemVolumeRange[0]
systemVolumeMax = systemVolumeRange[1]

# Init Volume Control
volume = 0
volumeBar = 400
volumePercent = 0

while True:
    success, image = capture.read()

    # Image Processing
    image = detector.findHands(image)
    landmarkList = detector.findPosition(image, draw=False)
    
    if len(landmarkList) != 0:

        # landmarkList[4] = Thumb
        # landmarkList[8] = Forefinger
        # print(landmarkList[4], landmarkList[8])

        # Thumb Coordinates
        x1, y1 = landmarkList[4][1], landmarkList[4][2]
        # Forefinger Coodinates
        x2, y2 = landmarkList[8][1], landmarkList[8][2]
        # Center Dot Coordinates Between Thumb and Forefinger
        cx, cy = (x1+x2)//2, (y1+y2)//2

        # Drawing Dots
        cv.circle(image, (x1, y1), 7, (255, 0, 0), cv.FILLED)
        cv.circle(image, (x2, y2), 7, (255, 0, 0), cv.FILLED)
        cv.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv.circle(image, (cx, cy), 7, (255, 0, 0), cv.FILLED)

        # Volume Bar Size
        barSize = math.hypot(x2-x1, y2-y1)
        print(barSize)

        # Hand Dots Distance Range = 50~300
        # Volume Bar
        volumeBar = np.interp(barSize, [50, 300], [400, 150])
        # Volume Percent
        volumePercent = np.interp(barSize, [50, 300], [0, 100])

        # Interpolating to system volume range
        volume = np.interp(barSize, [50, 300], [systemVolumeMin, systemVolumeMax])

        # Set System Volume
        systemVolume.SetMasterVolumeLevel(volume, None)

        # Minimum Volume Reached
        if barSize < 50:
            cv.circle(image, (cx, cy), 7, (255, 0, 255), cv.FILLED)

    # Drawing Volume Bar
    cv.rectangle(image, (50, 150), (60, 400), (0, 255, 0), 3)
    cv.rectangle(image, (50, int(volumeBar)), (60, 400), (0, 255, 0), cv.FILLED)
    cv.putText(image, f"{int(volumePercent)} %", (40, 450), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    # FPS Calcule
    cTime = time.time() 
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv.putText(image, f"FPS: {int(fps)}", (40, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    # Health Validation
    if not success:
        print('[FATAL ERROR] Generic Fail')
        exit()

    # Plot Image
    cv.imshow('image', image)

    # Sleep 1ms per Loop
    cv.waitKey(1)
