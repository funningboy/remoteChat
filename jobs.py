
import cv2
import numpy as np


class ImageProc(object):
    def __init__(self):
        pass

    def run(self):
        pass

class DetectCircle(ImageProc):
    """ detect circle """

    def __init__(self):
        super(DetectCircle, self).__init__()

    def run(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=5, maxRadius=20)
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.circle(img, (i[0],i[1]),i[2],(0,255,0),1)
                cv2.circle(img, (i[0],i[1]),2,(0,0,255),3)
        return img


class DetectEdge(ImageProc):
    """ detect edge """

    def __init__(self):
        super(DetectEdge, self).__init__()

    def run(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, 500, 1000, apertureSize=5)
        img /= 2
        img[edge != 0] = (0, 255, 0)
        return img


