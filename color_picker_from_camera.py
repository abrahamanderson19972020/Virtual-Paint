import cv2
import numpy as np
frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3,frameWidth) # set width
cap.set(4,frameHeight)  # set height
cap.set(19,150) #set the brigtness as 100"


def empty(b):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
#Step 1: Creating Trackbars for Hue, Saturation and Values of HSV colro
cv2.createTrackbar("Hue Min","TrackBars",0,179,empty) # 0 minimum 179 maximum value and empty is a just function
cv2.createTrackbar("Hue Max","TrackBars",179,179,empty)
cv2.createTrackbar("Sat Min","TrackBars",0,255,empty)
cv2.createTrackbar("Sat Max","TrackBars",255,255,empty)
cv2.createTrackbar("Val Min","TrackBars",0,255,empty)
cv2.createTrackbar("Val Max","TrackBars",255,255,empty)

while True:
    success, frame = cap.read()
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    hue_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    sat_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    sat_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    val_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    val_max = cv2.getTrackbarPos("Val Max", "TrackBars")
    print(hue_min, hue_max, sat_min, sat_max, val_min, val_max)
    lower = np.array([hue_min, sat_min, val_min])
    upper = np.array([hue_max, sat_max, val_max])
    mask = cv2.inRange(src=imgHSV, lowerb=lower, upperb=upper)
    result =cv2.bitwise_and(frame,frame, mask = mask)

    mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([frame,mask,result])
    cv2.imshow("Horizontal Stacking", hStack)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyWindow()