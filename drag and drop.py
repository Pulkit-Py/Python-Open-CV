import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

cap = cv2.VideoCapture(2)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=1)
coloR = (255,0,255)
cx,cy,w,h = 100,100, 200,200 

class DragRect():
    def __init__(self,poscenter, size=[200,200]):
        self.poscenter = poscenter
        self.size = size
    def update(self,cursor):
        cx ,cy = self.poscenter
        w ,h = self.size
        if cx-w//2 <cursor[0]< cx+w//2 and cy-h//2 <cursor[1] <cy+h//2:
            self.poscenter = cursor
     

rectlist = []
for x in range(5):
    rectlist.append(DragRect([x*250+150,150]))

while True:
    success , img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList , _ = detector.findPosition(img)
    if lmList:
        l , _ ,_ = detector.findDistance(8,12,img)
        print(l)
        if l<50:
            cursor = lmList[8]
            for rect in rectlist:
                rect.update(cursor)
    imgNew = np.zeros_like(img,np.uint8)
    for rect in rectlist:
        cx ,cy = rect.poscenter
        w ,h = rect.size 
        cv2.rectangle(imgNew,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),coloR,cv2.FILLED)
        cvzone.cornerRect(imgNew,(cx-w//2,cy-h//2,w,h),20,rt=0)
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv2.addWeighted(img,alpha,imgNew, 1-alpha,0)[mask]

    cv2.imshow("Image",out)
    cv2.waitKey(1)
    if  0xFF == ord('q'):
        break
