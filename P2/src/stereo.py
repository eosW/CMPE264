import numpy as np
import cv2
from matplotlib import pyplot as plt


def plane_sweeping(img1, img2, img3, R12, R13, r12, r13, K):
    """
    :param img1: image, greyscale
    :param img2: image, greyscale
    :param img3: image, greyscale
    :param np.matrix R12:
    :param np.matrix R13:
    :param np.matrix r12:
    :param np.matrix r13:
    :param np.matrix K:
    :return None:
    """
    # constants:
    delta = 5
    setplength = 10

    # derived values:
    kernel = np.ones((delta * 2 + 1, delta * 2 + 1))
    f = K[0, 0]
    r21 = -r12
    r31 = -r13

    minSAD12, minSAD13, minSAD123 = None, None, None
    depth12, depth13, depth123 = None, None, None
    for i in range(1, setplength, np.floor(f)):
        d = f / i
        H12 = R12 - (r21 * np.mat([0, 0, -1]) / d)
        H13 = R13 - (r31 * np.mat([0, 0, -1]) / d)
        M21 = K * H12.I * K.I
        M31 = K * H13.I * K.I
        warp2 = cv2.warpPerspective(img2, M21, img1.shape)
        warp3 = cv2.warpPerspective(img3, M31, img1.shape)
        AD12 = np.abs(img1 - warp2)
        AD13 = np.abs(img1 - warp3)
        SAD12 = cv2.filter2D(AD12, -1, kernel)
        SAD13 = cv2.filter2D(AD13, -1, kernel)
        SAD123 = SAD12 + SAD13
        if not minSAD12:
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
            depth12[update12] = d
            depth13[update13] = d
            depth123[update123] = d
            minSAD12[update12] = SAD12[update12]
            minSAD13[update13] = SAD13[update13]
            minSAD123[update123] = SAD123[update123]

    plt.subplot(131)
    plt.imshow(depth12, cmap='cool', clim=[0, f])
    plt.colorbar()
    plt.subplot(132)
    plt.imshow(depth13, cmap='cool', clim=[0, f])
    plt.colorbar()
    plt.subplot(133)
    plt.imshow(depth123, cmap='cool', clim=[0, f])
    plt.colorbar()

    plt.show()
