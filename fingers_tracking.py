
# Imports
import cv2 as cv
import time
import hand_track_module # Local Library

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
detector = hand_track_module.HandsDetector(detecConf=0.7)

#                      Fingers Pattern
#           [ Thumb, First, Second, Third, Fourth ]
one       = [ False, True,  False,  False, False  ]
two       = [ False, True,  True,   False, False  ]
three     = [ False, True,  True,   True,  False  ]
four      = [ False, True,  True,   True,  True   ]
five      = [ True,  True,  True,   True,  True   ]
rock      = [ False, True,  False,  False, True   ]
hangloose = [ True,  False, False,  False, True   ]

while True:
    success, image = capture.read()

    # Image Processing
    image = detector.findHands(image)
    landmarkList = detector.findPosition(image, draw=False)
    
    # If Hand Detected
    if len(landmarkList) != 0:
        
        fingersTrack = detector.fingersTracking(landmarkList)
        print(fingersTrack)

        if fingersTrack == rock:
            cv.putText(image, "ROCK", (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        
        elif fingersTrack == hangloose:
            cv.putText(image, "HANGLOOSE", (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        
        elif fingersTrack == one:
            cv.putText(image, "1", (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

        elif fingersTrack == two:
            cv.putText(image, "2", (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        
        elif fingersTrack == three:
            cv.putText(image, "3", (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        
        elif fingersTrack == four:
            cv.putText(image, "4", (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)
        
        elif fingersTrack == five:
            cv.putText(image, "5", (100, 200), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

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
