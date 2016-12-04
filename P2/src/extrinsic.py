import numpy as np
from matplotlib import pyplot as plt

def recover(E,K,inlierl,inlierr,imgl,imgr):
    """
    :param np.matrix E:
    :param np.matrix K:
    :param np.ndarray inlierl: each row is one inlier in left image
    :param np.ndarray inlierr: each row is the corresponding inlier in right image
    :param imgl: left image, colored
    :param imgr: right image, colored
    :return:
    """
    W = np.matrix('0 -1 0;1 0 0;0 0 1')

    f = K[0,0]

    inlierlh = np.ones((inlierl.size[0],inlierl.size[0]+1),np.float32)
    inlierrh = np.ones((inlierr.size[0],inlierr.size[0]+1),np.float32)
    inlierlh[:,:-1] = inlierl
    inlierrh[:,:-1] = inlierr

    U,S,V = np.linalg.svd(E)
    du,dv = np.linalg.det(U),np.linalg.det(U)
    print 'du,dv={:f},{:f}'.format(du,dv)
    if du==-1 and dv==-1:
        return
    elif du==-1 or dv==-1:
        U,S,V = np.linalg.svd(-E)
    r1 = V[:,3]
    r2 = -r1
    R1 = U*W*V.T
    R2 = U*W.T*V.T

    for R,r in ((R1,r1),(R2,r1),(R1,r2),(R2,r2)):
        normel = r.T/np.linalg.norm(r)
        orth1 = np.matrix([normel[0,1],-normel[0,0],0])
        orth2 = np.matrix([0,-normel[0,2],normel[0,1]])
        Rll = np.vstack((normel,orth1,orth2))
        Rrr = Rll*R.T
        Hl = K*Rll*K.I
        Hr = K*Rrr*K.I
        inlierlph = Hl*inlierlh.T
        inlierrph = Hr*inlierrh.T
        inlierlp = (inlierlph/inlierlph[2,:])[0:2,:]
        inlierrp = (inlierrph/inlierrph[2,:])[0:2,:]
        depth = f*np.linalg.norm(r)/(inlierlp[0,:]-inlierrp[0,:])
        if np.all(depth>0):
            inlierlcl = K.I*inlierlh.T
            inlierlcr = R*inlierlcl+r
            inlierlrh = K*inlierlcr
            inlierlr = (inlierlrh/inlierlrh[2,:])[0:2,:].T.A
            plt.imshow(imgr)
            plt.scatter(inlierr[:,0],inlierr[:,1],c='b',marker='+')
            plt.scatter(inlierlr[:,0],inlierlr[:,1],c='b',marker='x')
            plt.show()
            rmse = np.sqrt(2*np.mean(np.square(inlierlr-inlierr)))
            print 'rmse:{:f}'.format(rmse)
            print 'depth:'
            print '\n'.join(['{:d},{:d}):{:d}'.format(t[0],t[1],t[2]) for t in np.hstack((inlierl,depth.T)).A])
            return R,r