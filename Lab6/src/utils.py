from abc import ABC, abstractmethod

import cv2 as cv
import numpy as np


def haris_corner_detector(img, dilate=True):
    gray = np.float32(cv.cvtColor(img, cv.COLOR_BGR2GRAY))
    mask = cv.cornerHarris(gray, 2, 3, 0.04)
    if dilate:
        mask = cv.dilate(mask, None)
    final = img.copy()
    final[mask > 0.01 * mask.max()] = (0, 0, 255)
    return final, mask


def sift_detector(img):
    haris, mask = haris_corner_detector(img, dilate=True)
    kp = np.argwhere(mask > 0.01 * mask.max())
    kp = [cv.KeyPoint(float(x[1]), float(x[0]), 13) for x in kp]
    sift = cv.SIFT_create()
    sift.compute(haris, kp)
    cv.drawKeypoints(haris, kp, haris)
    return haris


def select_roi(img):
    x, y, w, h = cv.selectROI(img)
    cv.destroyAllWindows()
    img = img.copy()[y: y + h, x: x + w]
    return img


class Tracker(ABC):
    @abstractmethod
    def init(self, frame, roi):
        ...

    @abstractmethod
    def update(self, frame):
        ...


class MeanShiftTracker(Tracker):
    bbox = None
    roi_hist = None

    def init(self, frame, bbox):
        x, y, w, h = bbox
        roi = frame[y:y + h, x:x + w]
        roi_hist = cv.calcHist([roi], [0], None, [256], [0, 256])
        roi_hist = cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        self.roi_hist = roi_hist
        self.bbox = bbox

    def update(self, frame):
        term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], self.roi_hist, [0, 256], 1)
        return cv.meanShift(dst, self.bbox, term_crit)


class CamShiftTracker(Tracker):
    bbox = None
    roi_hist = None

    def init(self, frame, bbox):
        x, y, w, h = bbox
        roi = frame[y:y + h, x:x + w]
        roi_hist = cv.calcHist([roi], [0], None, [256], [0, 256])
        roi_hist = cv.normalize(roi_hist, roi_hist, 0, 255, cv.NORM_MINMAX)
        self.roi_hist = roi_hist
        self.bbox = bbox

    def update(self, frame):
        term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv], [0], self.roi_hist, [0, 256], 1)
        return cv.CamShift(dst, self.bbox, term_crit)

