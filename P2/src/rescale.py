import numpy as np
from scipy import optimize
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def rescale(r121, r231, r311):
    """
    :param np.matrix r212:
    :param np.matrix r323:
    :param np.matrix r313:
    :param np.matrix R12:
    :param np.matrix R13:
    :return float,float: beta and gamma
    """

    v12 = r121 / np.linalg.norm(r121)
    v23 = r231 / np.linalg.norm(r231)
    v31 = r311 / np.linalg.norm(r311)

    theta = np.array([1, 1])

    def norms(theta):
        return np.sum(np.square(v12 + theta[0] * v23 + theta[1] * v31))

    res = optimize.minimize(norms, theta, method='bfgs')

    opttheta = res.x

    print 'origin norm: {:f}'.format(norms([1, 1]))
    print 'optimized norm: {:f}'.format(norms([opttheta[0], opttheta[1]]))

    p = np.hstack(([[0],[0],[0]],v12,v12+opttheta[0]*v23,v12+opttheta[0]*v23+opttheta[1]*v31))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(p[0,:],p[1,:],p[2,:])
    plt.show()

    return opttheta[0], opttheta[1]
