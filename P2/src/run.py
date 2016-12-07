import numpy as np
import cv2
from calibration import calibration
from epipolar import epipolar
from extrinsic import recover
from rescale import rescale
from stereo import plane_sweeping

K,dist = calibration()
K = np.mat(K)
img1 = cv2.imread('cali1.jpg', cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread('cali2.jpg', cv2.IMREAD_GRAYSCALE)
img3 = cv2.imread('cali3.jpg', cv2.IMREAD_GRAYSCALE)

E12,inlier121,inlier122 = epipolar(K,img1,img2)
E13,inlier131,inlier133 = epipolar(K,img1,img3)
E23,inlier232,inlier233 = epipolar(K,img2,img3)
E12 = np.mat(E12)
E13 = np.mat(E13)
E23 = np.mat(E23)


R12,r121,r212 = recover(E12,K,inlier121,inlier122,img1,img2)
print R12,r212
R13,r131,r313 = recover(E13,K,inlier131,inlier133,img1,img3)
print R13,r313
R23,r232,r323 = recover(E23,K,inlier232,inlier233,img2,img3)
print R23,r323
R31 = -R13
R32 = -R23
r231 = -R12*r232+r212
r311 = -r131

beta,gamma = rescale(r121.A,r231.A,r311.A)
print beta,gamma
r313 = gamma*r313

plane_sweeping(img1,img2,img3,R12,R13,r212.A,r313.A,K)
