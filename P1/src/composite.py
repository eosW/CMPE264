import cv2
import numpy as np
from Calibration import Calibration


class composite:
    def __init__(self):
        self.a1 = 9
        self.a2 = 30
        self.calibrator = Calibration()
        self.img0 = self.linearize(cv2.imread("../pic_highcontrust/180.jpg", cv2.IMREAD_COLOR))
        self.img1 = self.linearize(cv2.imread("../pic_highcontrust/20.jpg", cv2.IMREAD_COLOR))
        self.img2 = self.linearize(cv2.imread("../pic_highcontrust/6.jpg", cv2.IMREAD_COLOR))
        self.cap = self.calibrator.get_true_b([255, 255, 255])

    def linearize(self, img):
        imgl = np.zeros(img.shape, np.float32)
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                imgl[i, j] = self.calibrator.get_true_b(img[i, j])
        return imgl

    def alg1(self):
        imgc = np.zeros(self.img0.shape, np.float32)
        for i in range(self.img0.shape[0]):
            for j in range(self.img0.shape[1]):
                if all(self.img2[i, j] < self.cap):
                    imgc[i, j] = self.img2[i, j] / self.a2
                elif all(self.img1[i, j] < self.cap):
                    imgc[i, j] = self.img1[i, j] / self.a1
                else:
                    imgc[i, j] = self.img0[i, j]
        return imgc

    def alg2(self):
        imgc = np.zeros(self.img0.shape, np.float32)
        for i in range(self.img0.shape[0]):
            for j in range(self.img0.shape[1]):
                if all(self.img2[i, j] < self.cap):
                    imgc[i, j] = (self.img2[i, j] / self.a2 + self.img1[i, j] / self.a1 + self.img0[i, j]) / 3
                elif all(self.img1[i, j] < self.cap):
                    imgc[i, j] = (self.img1[i, j] / self.a1 + self.img0[i, j]) / 2
                else:
                    imgc[i, j] = self.img0[i, j]
        return imgc

    def alg3(self):
        imgc = np.zeros(self.img0.shape, np.float32)
        for i in range(self.img0.shape[0]):
            for j in range(self.img0.shape[1]):
                if all(self.img2[i, j] < self.cap):
                    imgc[i, j] = self.img2[i, j] * self.a2 / (1 + self.a1 ** 2 + self.a2 ** 2) + self.img1[
                                                                                               i, j] * self.a1 / (
                                                                                               1 + self.a1 ** 2 + self.a2 ** 2) + \
                           self.img0[i, j] / (1 + self.a1 ** 2 + self.a2 ** 2)
                elif all(self.img1[i, j] < self.cap):
                    imgc[i, j] = self.img1[i, j] * self.a1 / (1 + self.a1 ** 2) + self.img0[i, j] / (
                        1 + self.a1 ** 2)
                else:
                    imgc[i, j] = self.img0[i, j]
        return imgc
