import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt


def epipolar(K,img1,img2):
    # ap = argparse.ArgumentParser()
    # ap.add_argument("-q", "--query", required=True, help="Path to the image")
    # ap.add_argument("-i", "--train", required=True, help="Path to the image")
    # args = vars(ap.parse_args())
    # img1 = cv2.imread(args["query"], 0)
    # img2 = cv2.imread(args["train"], 0)
    surf = cv2.xfeatures2d.SURF_create()
    kp1, des1 = surf.detectAndCompute(img1, None)
    kp2, des2 = surf.detectAndCompute(img2, None)
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=100)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    good = []
    pts1 = []
    pts2 = []
    matches = flann.knnMatch(des1, des2, k=2)
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.5 * n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
    pts1 = np.int32(pts1)
    pts2 = np.int32(pts2)
    E, mask = cv2.findEssentialMat(pts1, pts2, K)
    F, _ = cv2.findFundamentalMat(pts1, pts2)
    pts1in = pts1[mask.ravel()==1]
    pts2in = pts2[mask.ravel()==1]
    print 'the essential matrix between two images is:', E

    pts1ot = pts1[mask.ravel()!=1]
    pts2ot = pts2[mask.ravel()!=1]

    def drawlines(img1, img2, lines, pts1, pts2, pts3, pts4):
        ''' img1 - image on which we draw the epilines for the points in img2
            lines - corresponding epilines '''
        r, c = img1.shape
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        for pt3,pt4 in zip(pts3, pts4):
            img1 = cv2.circle(img1,tuple(pt3),5,(0,0,0),-1)
            img2 = cv2.circle(img2,tuple(pt4),5,(0,0,0),-1)
        for r, pt1, pt2 in zip(lines, pts1, pts2):
            color1 = (255,0,0)
            color2 = (0,0,255)
            x0, y0 = map(int, [0, -r[2] / r[1]])
            x1, y1 = map(int, [c, -(r[2] + r[0] * c) / r[1]])
            img1 = cv2.line(img1, (x0, y0), (x1, y1), color2, 1)
            img1 = cv2.circle(img1, tuple(pt1), 5, color1, -1)
            img2 = cv2.circle(img2, tuple(pt2), 5, color1, -1)
        return img1, img2

    lines1 = cv2.computeCorrespondEpilines(pts2in.reshape(-1, 1, 2), 2, F)
    lines1 = lines1.reshape(-1, 3)
    img5, img6 = drawlines(img1, img2, lines1, pts1in, pts2in, pts1ot, pts2ot)
    lines2 = cv2.computeCorrespondEpilines(pts1in.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)
    img3, img4 = drawlines(img2, img1, lines2, pts2in, pts1in, pts2ot, pts1ot)
    plt.subplot(121), plt.imshow(img5)
    plt.subplot(122), plt.imshow(img3)
    plt.show()

    return E,pts1in,pts2in
