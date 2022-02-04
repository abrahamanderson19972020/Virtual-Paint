import cv2
import numpy as np
frameWidth = 1000
frameHeight = 900

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth) # set width
cap.set(4,frameHeight)  # set height
cap.set(10,150) #set the brigtness as 100"

#This is the list of colors we want to detect
colors=[[70,60,106,98,178,255], #green
        [16,13,255,32,88,255],  #Orange
        [77,28,254,107,210,255],  #Blue
        [115,78,255,179,253,255], #Red
        [136,39,206,161,167,255], #Purple
        [20,17,253,33,74,255] # Yellow
        ]
# BGR Colors
colorValues = [[0,255,0],  #Green
               [51,153,255], #Orange
               [255,0,0],#Blue
               [0,0,255], #Red
               [153,0,153], #Purple
               [51,255,255]] # Yellow
color_names=["Green","Orange","Blue"]
myPoints = [] # [x,y,colorIndex]
def findColor(img,colors,colorValues):
    count = 0
    newPoints = []
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(src=imgHSV,lowerb=lower,upperb=upper)
        x,y = getContours(mask)
        cv2.circle(frameResult,(x,y),10,(colorValues[count]),cv2.FILLED)
        #cv2.imshow(color_names[count],mask)
        if x!= 0 and y!= 0:
            newPoints.append([x,y,count])

        count +=1
    return newPoints
def getContours(img):
    contours, hiearchy = cv2.findContours(img,mode=cv2.RETR_EXTERNAL,method=cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        areaOFInterest = cv2.contourArea(cnt)
        print(areaOFInterest)
        if areaOFInterest > 500: # We put a thresholf with if statement
            cv2.drawContours(frameResult, contours=cnt, contourIdx=-1, color=(0, 0, 0), thickness=1)
            perimeter = cv2.arcLength(cnt,True) #This get all perimete
            approx = cv2.approxPolyDP(cnt,0.02*perimeter,True)
             #This gives the corners of each contour

            x,y,w,h = cv2.boundingRect(approx) #This will us the width and height of each object or contours
    return x+w//2, y #we send the center and top point of the image
def drawOnCanves(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(frameResult, (point[0], point[1]), 10, (myColorValues[point[2]]), cv2.FILLED)


while True:
    success, frame = cap.read()
    frameResult = frame.copy()
    newPoints = findColor(frame,colors,colorValues)
    if len(newPoints) != 0:
        for point in newPoints:
            myPoints.append(point)
    if len(myPoints) != 0:
        drawOnCanves(myPoints,colorValues)
    cv2.imshow("Video Frame",frameResult)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break