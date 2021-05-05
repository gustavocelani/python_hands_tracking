
# Imports
import cv2 as cv
import mediapipe as mp

# Hands Detector Class
class HandsDetector():

    # Init
    def __init__(self, mode=False, maxHands=2, detecConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detecConf = detecConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detecConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    # Find Hands
    def findHands(self, image, draw=True):

        # Hands Dots
        imgRGB = cv.cvtColor(image, cv.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        # Detect Hands
        if self.results.multi_hand_landmarks:  # detectar as mãos
            
            # For each Hand
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    # Draw Connections
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)

        return image

    # Find Position
    def findPosition(self, image, handNo=0, draw=True):

        landmarkList = []

        if self.results.multi_hand_landmarks:

            # Hands Array
            hands = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(hands.landmark):
                # print(id, lm)

                # X and Y Dots Coordinates
                h, w, c = image.shape

                # Circles on X and Y Dots
                cx, cy = int(lm.x*w), int(lm.y*h)

                # print(id, cx, cy)
                landmarkList.append([id, cx, cy])

                # Draw Circles
                if draw:
                    cv.circle(image, (cx, cy), 7, (255, 0, 0), cv.FILLED)

        return landmarkList

    # Fingers Tracking
    def fingersTracking(self, landmarkList):

        # Finger Opened = True
        # Finger Closed = False
        #
        # result[0] = Thumb
        # result[1] = First  Finger
        # result[2] = Second Finger
        # result[3] = Third  Finger
        # result[4] = Fourth Finger
        result = []

        # Thumb
        pseudoFixKeyPoint = landmarkList[2][1]
        result.append(not (landmarkList[3][1] < pseudoFixKeyPoint and landmarkList[4][1] < pseudoFixKeyPoint))

        # First Finger
        pseudoFixKeyPoint = landmarkList[6][2]
        result.append(landmarkList[7][2] < pseudoFixKeyPoint and landmarkList[8][2] < pseudoFixKeyPoint)

        # Second Finger
        pseudoFixKeyPoint = landmarkList[10][2]
        result.append(landmarkList[11][2] < pseudoFixKeyPoint and landmarkList[12][2] < pseudoFixKeyPoint)

        # Third Finger
        pseudoFixKeyPoint = landmarkList[14][2]
        result.append(landmarkList[15][2] < pseudoFixKeyPoint and landmarkList[16][2] < pseudoFixKeyPoint)

        # Fourth Finger
        pseudoFixKeyPoint = landmarkList[18][2]
        result.append(landmarkList[19][2] < pseudoFixKeyPoint and landmarkList[20][2] < pseudoFixKeyPoint)

        return result
