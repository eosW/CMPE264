import cv2
import numpy as np

from Calibration import Calibration

class ToneMapping:
    def __init__(self):
        self.tome_mapper = cv2.createTonemapDurand(gamma=2.2)

    def map(self, img):
        img2 = self.tome_mapper.process(img)
        return np.clip(img2*255, 0, 255).astype('uint8')

