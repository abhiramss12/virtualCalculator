import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Button class
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        x, y = self.pos
        cv2.rectangle(img, self.pos, (x + self.width, y + self.height), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, self.value, (x + 20, y + 60), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

    def checkClick(self, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            return True
        return False


# Create Buttons
buttonList = []
values = [['7', '8', '9', '/'],
          ['4', '5', '6', '*'],
          ['1', '2', '3', '-'],
          ['C', '0', '=', '+']]

for i in range(4):
    for j in range(4):
        x = 100 * j + 800
        y = 100 * i + 150
        buttonList.append(Button((x, y), 100, 100, values[i][j]))

myEquation = ''
delayCounter = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, (1280, 720))

    # Draw white background for calculator
    cv2.rectangle(img, (800, 50), (1200, 130), (255, 255, 255), cv2.FILLED)

    # Detect hand
    hands, img = detector.findHands(img)

    # Draw Buttons
    for button in buttonList:
        button.draw(img)

    # Display equation
    cv2.putText(img, myEquation, (810, 120), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    if hands:
        lmList = hands[0]['lmList']
        x, y = lmList[8][0], lmList[8][1]  # Index finger tip
        fingers = detector.fingersUp(hands[0])

        # Check click
        if fingers[1] == 1 and fingers[2] == 0:  # Only index finger up
            for i, button in enumerate(buttonList):
                if button.checkClick(x, y) and delayCounter == 0:
                    value = button.value
                    if value == 'C':
                        myEquation = ''
                    elif value == '=':
                        try:
                            myEquation = str(eval(myEquation))
                        except:
                            myEquation = 'Error'
                    else:
                        myEquation += value
                    delayCounter = 1

    # Delay counter for debouncing clicks
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 10:
            delayCounter = 0

    cv2.imshow("Virtual Calculator", img)
    cv2.waitKey(1)
