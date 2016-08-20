import cv2
import numpy as np
# from detectPaper import AFourDetector

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self, params):
        success, image = self.video.read()
        image = cv2.flip(image, 1)
        if (params['camera'] == 'camera2'):

            image = self.blabla(image, params)
        else:
            image = self.hulio(image, params)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_new(self, old):
        new = np.ones(old.shape, np.uint8)
        cv2.bitwise_not(new,new)
        return new

    def hulio(self, image, params):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray


    def blabla(self, image, params):
        # lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        # l, a, b = cv2.split(lab)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        gray = cv2.Canny(gray, params['range1'], params['range2'])
        # (T, threshInv) = cv2.threshold(gray, params['range1'], params['range2'], cv2.THRESH_BINARY_INV)
        (cnts, _) = cv2.findContours(gray.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
        screenCnt = None

        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)
         
            # if our approximated contour has four points, then
            # we can assume that we have found our screen
            if len(approx) == 4:
                screenCnt = approx
                break

        cv2.drawContours(image, screenCnt, -1, (0, 255, 0), 3)
# loop over each of the individual channels and display them
        
        # gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        # rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (params['range1'], 10))
        # squareKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)
        # opening = cv2.morphologyEx(tophat, cv2.MORPH_OPEN, squareKernel)
        # light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, rectKernel)
        #light = cv2.threshold(light, params['range1'], 255, cv2.THRESH_BINARY)[1]

        # gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        # (T, threshInv) = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        return gray