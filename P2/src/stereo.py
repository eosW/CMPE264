import numpy as np
import cv2
from matplotlib import pyplot as plt


def plane_sweeping(img1, img2, img3, R12, R13, r21, r31, K):
    """
    :param img1: image, greyscale
    :param img2: image, greyscale
    :param img3: image, greyscale
    :param np.matrix R12:
    :param np.matrix R13:
    :param np.ndarray r12:
    :param np.ndarray r13:
    :param np.matrix K:
    :return None:
    """
    # constants:
    delta = 5
    setplength = 10

    # derived values:
    kernel = np.ones((delta * 2 + 1, delta * 2 + 1))/(delta*2+1)**2
    f = K[0, 0]

    minSAD12, minSAD13, minSAD123 = None, None, None
    depth12, depth13, depth123 = None, None, None
    for i in range(1, int(np.floor(f)), setplength):
        d = f * np.linalg.norm(r21) / i
        H12 = R12 - (r21 * np.mat([0, 0, -1]) / d)
        H13 = R13 - (r31 * np.mat([0, 0, -1]) / d)
        M21 = K * H12.I * K.I
        M31 = K * H13.I * K.I
        warp2 = cv2.warpPerspective(img2, M21, (img1.shape[1],img1.shape[0]))
        warp3 = cv2.warpPerspective(img3, M31, (img1.shape[1],img1.shape[0]))
        AD12 = cv2.absdiff(img1, warp2)
        AD13 = cv2.absdiff(img1, warp3)
        SAD12 = cv2.filter2D(AD12, -1, kernel)
        SAD13 = cv2.filter2D(AD13, -1, kernel)
        SAD123 = (SAD12 + SAD13)/2
        if minSAD12 is None:
            minSAD12 = SAD12
            minSAD13 = SAD13
            minSAD123 = SAD123
            depth12 = np.full(SAD12.shape, d, np.float32)
            depth13 = np.full(SAD12.shape, d, np.float32)
            depth123 = np.full(SAD12.shape, d, np.float32)
        else:
            update12 = SAD12 < minSAD12
            update13 = SAD13 < minSAD13
            update123 = SAD123 < minSAD123
            depth12[update12] = i
            depth13[update13] = i
            depth123[update123] = i
            minSAD12[update12] = SAD12[update12]
            minSAD13[update13] = SAD13[update13]
            minSAD123[update123] = SAD123[update123]
        # plt.subplot(231)
        # plt.imshow(warp2, cmap='gray')
        # plt.subplot(232)
        # plt.imshow(img1, cmap='gray')
        # plt.subplot(233)
        # plt.imshow(SAD12, cmap='gray')
        # plt.subplot(234)
        # plt.imshow(AD12, cmap='gray')
        # plt.subplot(235)
        # plt.imshow(depth12, cmap='gray')
        # plt.subplot(236)
        # plt.imshow(minSAD12, cmap='gray')
        # plt.show()

    plt.subplot(221)
    plt.imshow(depth12, cmap='coolwarm', clim=[0, f])
    plt.colorbar()
    plt.subplot(222)
    plt.imshow(depth13, cmap='coolwarm', clim=[0, f])
    plt.colorbar()
    plt.subplot(223)
    plt.imshow(depth123, cmap='coolwarm', clim=[0, f])
    plt.colorbar()
    plt.subplot(224)
    plt.imshow(img1, cmap='gray')

    plt.show()
