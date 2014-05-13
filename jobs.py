
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


class DetectFace(ImageProc):
    """ detect face """

    def __init__(self):
        super(DetectFace, self).__init__()
        self._cascade_fn, self._nested_fn = self._train_data()

    def run(self, img):
        """ detect human face """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        rects = self._detect(gray,  self._cascade_fn)
        self._draw_rects(img, rects)
        for x1, y1, x2, y2 in rects:
            roi = gray[y1:y2, x1:x2]
            img_roi = img[y1:y2, x1:x2]
            subrects = self._detect(roi.copy(), self._nested_fn)
            img = self._draw_rects(img, subrects)
        return img

    def _train_data(self,
            cascade_fn='./data/haarcascades/haarcascade_frontalface_alt.xml',
            nested_fn='./data/haarcascades/haarcascade_eye.xml'):
        _cascade_fn = cv2.CascadeClassifier(cascade_fn)
        _nested_fn  = cv2.CascadeClassifier(nested_fn)
        return _cascade_fn, _nested_fn

    def _detect(self, img, cascade):
        rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(rects) == 0:
            return []
        rects[:,2:] += rects[:,:2]
        return rects

    def _draw_rects(self, img, rects):
        for x1, y1, x2, y2 in rects:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        return img



