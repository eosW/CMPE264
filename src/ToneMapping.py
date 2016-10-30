import cv2
import numpy as np

from Calibration import Calibration

class ToneMapping:
    def __init__(self):
        self.tome_mapper = cv2.createTonemap(gamma=1)

    def map(self, img):
        return self.tome_mapper.process(img)

img = cv2.imread('../pic_whitepaper/180.JPG', cv2.IMREAD_COLOR)
c = Calibration()
img2 = np.zeros(img.shape,np.float32)
for i in range(0,img.shape[0]):
    for j in range(0,img.shape[1]):
        img2[i,j] = c.get_true_b(img[i,j])
t = ToneMapping()
img3 = t.map(img2)
img4 = np.clip(img3*255, 0, 255).astype('uint8')
cv2.imwrite("test.jpg",img4)