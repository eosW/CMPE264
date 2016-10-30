import cv2
import numpy as np


a1 = 9
a2 = 30

def alg1():
    for i in range(img0.height):
        for j in range(img0.width):
            if img2[i,j]<=255:
                img0[i,j]=img2[i,j]/a2
            elif img1[i.j]<=255:
                img0[i,j]=img1[i,j]/a1
            else: 
                img0[i,j]=img0[i,j]
    cv2.imwrite("hdr1.jpg", img0)

def alg2():
    for i in range(img0.height):
        for j in range(img0.width):
            if img2[i,j]<=255:
                img0[i,j]=(img2[i,j]/a2+img1[i,j]/a1+img0[i,j])/3
            elif img1[i.j]<=255:
                img0[i,j]=(img1[i,j]/a1+img0[i,j])/2
            else: 
                img0[i,j]=img0[i,j]
    cv2.imwrite("hdr2.jpg", img0)

def alg3():
    for i in range(img0.height):
        for j in range(img0.width):
            if img2[i,j]<=255:
                img0[i,j]=img2[i,j]*a2/(1+a1**2+a2**2)+img1[i,j]*a1/(1+a1**2+a2**2)+img0[i,j]/(1+a1**2+a2**2)
            elif img1[i.j]<=255:
                img0[i,j]=img1[i,j]*a1/(1+a1**2)+img0[i,j]/(1+a1**2)
            else: 
                img0[i,j]=img0[i,j]
    cv2.imwrite("hdr3.jpg", img0)
