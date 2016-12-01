import os
import math

import cv2
import numpy as np
from scipy import stats,optimize
from matplotlib import pyplot


class Calibration:
    b = [0, 0, 0]
    g = [0, 0, 0]

    def __init__(self, plot=False):
        """
        load the pictures
        """
        x, y = [], []
        for fn in os.listdir('../pic_whitepaper'):
            rt = int(fn[:-4])
            img = cv2.imread('../pic_whitepaper/' + fn, cv2.IMREAD_COLOR)
            imgs = img[700:1000, 600:900, :]
            if not np.any(imgs == 255):
                x.append(1. / rt)
                y.append(np.mean(imgs, (0, 1)))
        x = np.array(x)
        y = np.array(y)
        ind = x.argsort()
        x = x[ind]
        y = y[ind, :]
        vln = np.vectorize(lambda i: math.log(i, math.e))
        lnx = vln(x)
        self.g[0], self.b[0], _, _, _ = stats.linregress(lnx, vln(y[:, 0]))
        self.g[1], self.b[1], _, _, _ = stats.linregress(lnx, vln(y[:, 1]))
        self.g[2], self.b[2], _, _, _ = stats.linregress(lnx, vln(y[:, 2]))
        cap = np.array([255**self.g[0], 255**self.g[1], 255**self.g[2]],np.float32)
        self.scale = cap/min(cap)
        if not plot:
            return
        pyplot.xlabel('ln T(s)')
        pyplot.ylabel("ln B'")
        pyplot.plot(lnx, vln(y[:, 0]), 'bo-')
        pyplot.plot(lnx, self.g[0]*lnx+self.b[0], 'b--')
        pyplot.plot(lnx, vln(y[:, 1]), 'go-')
        pyplot.plot(lnx, self.g[1]*lnx+self.b[1], 'g--')
        pyplot.plot(lnx, vln(y[:, 2]), 'ro-')
        pyplot.plot(lnx, self.g[2]*lnx+self.b[2], 'r--')
        pyplot.show()
        pyplot.cla()
        pyplot.xlabel('T(s)')
        pyplot.ylabel("cB'^g")
        tb = np.zeros(y.shape)
        tb[:, 0] = y[:, 0] ** self.g[0]/self.scale[0]
        tb[:, 1] = y[:, 1] ** self.g[1]/self.scale[1]
        tb[:, 2] = y[:, 2] ** self.g[2]/self.scale[2]
        pyplot.plot(x, tb[:, 0], 'bo-')
        pyplot.plot(x, tb[:, 1], 'go-')
        pyplot.plot(x, tb[:, 2], 'ro-')
        pyplot.show()
        pyplot.xlabel('B')
        pyplot.ylabel("cB'^g")
        x = range(255)
        y0 = x ** self.g[0]/self.scale[0]
        y1 = x ** self.g[1]/self.scale[1]
        y2 = x ** self.g[2]/self.scale[2]
        pyplot.plot(x, y0, 'b-')
        pyplot.plot(x, y1, 'g-')
        pyplot.plot(x, y2, 'r-')
        pyplot.show()

    def get_true_b(self, colors):
        """
        get the linear B
        :param ndarray, colors: input B of three colors in sequence of BGR, uint8
        :return: ndarray, linear B in BGR, float
        """
        return np.array([colors[0]**self.g[0]/self.scale[0], colors[1]**self.g[1]/self.scale[1], colors[2]**self.g[2]/self.scale[2]], np.float32)
        pass

if __name__ == "__main__":
    c = Calibration(True)
    print c.b
    print c.g
    print c.get_true_b([255,255,255])