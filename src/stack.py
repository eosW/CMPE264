import cv2
from Calibration import Calibration
import numpy as np
img0 = cv2.imread("180.jpg",0)
img1 = cv2.imread("20.jpg",0)
img2 = cv2.imread("6.jpg",0)

c = Calibration()

def linearize0():
    for i in range(img0.height):
        for j in range(img0.width):
      
            b=img0[i,j,0]
            g=img0[i,j,1]
            r=img0[i,j,2]
            img0[i,j]= c.get_true_b(b,g,r)

def linearize1():
    for i in range(img1.height):
        for j in range(img1.width):
      
            b=img1[i,j,0]
            g=img1[i,j,1]
            r=img1[i,j,2]
            img1[i,j]=c.get_true_b(b,g,r)

def linearize2():
    for i in range(img2.height):
        for j in range(img2.width):
      
            b=img2[i,j,0]
            g=img2[i,j,1]
            r=img2[i,j,2]
            img2[i,j]=c.get_true_b(b,g,r)

