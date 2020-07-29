import cv2
import numpy as np
import argparse
import imutils

class ShapeDetection:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.shape = "unidentified"
    def TampilVideo(self):
        while(True):
            ret,frame = self.camera.read()
            resized = imutils.resize(frame, width=300)
            # cv2.rectangle(frame,(50,50),(300,300),(0,0,255),0)   
            roi = frame[100:300, 100:300] 
            ratio = frame.shape[0] / float(resized.shape[0])
            if ret == True:
                gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)
                thresh = cv2.threshold(blurred, 100, 100, cv2.THRESH_BINARY)[1]

                cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                for c in cnts:
                    area = cv2.contourArea(c)
                    approx = cv2.approxPolyDP(c, 0.02*cv2.arcLength(c, True), True)
                    cX = approx.ravel()[0]
                    cY = approx.ravel()[1]
                    print(area)
                    if area >= 400:
                        shape = self.Detection(c)
                        c = c.astype("float")
                        c *= ratio
                        c = c.astype("int")
                        cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                        cv2.putText(frame, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 0), 2)
                cv2.imshow("Thresh",thresh)
                cv2.imshow("Frame",frame)
            k = cv2.waitKey(20) & 0xff
            if k == ord('q'):
                break 
        self.Close(self.camera)
    def Detection(self,counturs):
        peri = cv2.arcLength(counturs,True)
        self.approx = cv2.approxPolyDP(counturs,0.02 * peri, True)
        if len(self.approx) == 3:
            self.shape = "triangle"
        elif len(self.approx) == 4:
            (x, y, w, h) = cv2.boundingRect(self.approx)
            ar = w / float(h)
            self.shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        elif len(self.approx) == 5:
            self.shape = "pentagon"
        else:
            self.shape = "circle"
        return self.shape
    def Close(self,camera):
        camera.release()
        cv2.destroyAllWindows()

shapeDetection = ShapeDetection()
shapeDetection.TampilVideo()
 