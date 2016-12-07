import numpy as np
from matplotlib import pyplot as plt
import cv2

def recover(E,K,inlierl,inlierr,imgl,imgr):
    """
    :param np.matrix E:
    :param np.matrix K:
    :param np.ndarray inlierl: each row is one inlier in left image
    :param np.ndarray inlierr: each row is the corresponding inlier in right image
    :param imgr: right image, colored
    :return:
    """
    W = np.matrix('0 -1 0;1 0 0;0 0 1')

    f = K[0,0]

    inlierlh = np.ones((inlierl.shape[0],3),np.float32)
    inlierrh = np.ones((inlierr.shape[0],3),np.float32)
    inlierlh[:,:-1] = inlierl
    inlierrh[:,:-1] = inlierr

    U,S,V = np.linalg.svd(E)
    V = V.T
    du,dv = np.linalg.det(U),np.linalg.det(V)
    print 'du,dv={:f},{:f}'.format(du,dv)
    if du+1<1e-9 and dv+1<1e-9:
        print 'invalid E'
        return
    elif du+1<1e-9 or dv+1<1e-9:
        U,S,V = np.linalg.svd(-E)
        V = V.T
    rl1 = V[:,2]
    rl2 = -rl1
    rr1 = U[:,2]
    rr2 = -rr1
    R1 = U*W*V.T
    R2 = U*W.T*V.T

    for Rlr,rl,rr in ((R2,rl2,rr2),(R2,rl1,rr1),(R1,rl2,rr2),(R1,rl1,rr1)):
        co = f*Rlr[0,:]-inlierrh[:,0][:,None]*f*Rlr[2,:]
        depth = f*(co*rl)/np.sum(np.multiply(co,inlierlh*f*K.I.T),1)
        depth = depth.T
        if np.all(depth>0):
            inlierlcl = K.I*inlierlh.T
            inlierlcl = np.multiply(inlierlcl,(depth/inlierlcl[2,:]))

            coefx = -(K[0,0]*Rlr[0,:]*inlierlcl+np.multiply(K[0,2]-inlierr[:,0],Rlr[2,:]*inlierlcl))/(
                K[0,0]*rr[0]+np.multiply(K[0,2]-inlierr[:,0],rr[2]))
            coefy = -(K[1,1]*Rlr[1,:]*inlierlcl+np.multiply(K[1,2]-inlierr[:,1],Rlr[2,:]*inlierlcl))/(
                K[1,1]*rr[1]+np.multiply(K[1,2]-inlierr[:,1],rr[2]))
            avgcoef = np.mean(np.vstack((coefx,coefy)))
            print avgcoef
            inlierlcr = Rlr*inlierlcl+rr*avgcoef
            inlierlrh = K*inlierlcr
            inlierlr = (inlierlrh/inlierlrh[2,:])[0:2,:].T.A
            plt.imshow(imgr,cmap='gray')
            plt.scatter(inlierr[:,0],inlierr[:,1],c='b',marker='o')
            plt.scatter(inlierlr[:,0],inlierlr[:,1],c='r',marker='x')
            plt.show()
            rmse = np.sqrt(2*np.mean(np.square(inlierlr-inlierr)))
            if avgcoef<0:
                rl = -rl
                rr = -rr
            print 'rmse:{:f}'.format(rmse)
            print 'depth:'
            print '\n'.join(['{:f},{:f}):{:f}'.format(t[0],t[1],t[2]) for t in np.hstack((inlierl,depth.T)).A])
            return Rlr,rl,rr

    print 'no valid pair found'

