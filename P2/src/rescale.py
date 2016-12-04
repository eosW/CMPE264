import numpy as np
from scipy import optimize


def rescale(r212, r323, r313, R12, R13):
    """
    :param np.matrix r212:
    :param np.matrix r323:
    :param np.matrix r313:
    :param np.matrix R12:
    :param np.matrix R13:
    :return float,float: beta and gamma
    """
    r121 = -r212 * R12.I
    r231 = -r323 * R13.I
    r311 = r313 * R13.I

    v12 = r121 / np.linalg.norm(r121)
    v23 = r231 / np.linalg.norm(r231)
    v31 = r311 / np.linalg.norm(r311)

    theta = np.array([1, 1])

    def norms(beta, gamma):
        return v12 + beta * v23 + gamma * v31

    res = optimize.minimize(norms, theta, method='l-bfgs-b')

    opttheta = res.x

    print 'origin norm: {:f}'.format(norms(1, 1))
    print 'optimized norm: {:f}'.format(norms(opttheta[0], opttheta[1]))

    return opttheta[0], opttheta[1]
