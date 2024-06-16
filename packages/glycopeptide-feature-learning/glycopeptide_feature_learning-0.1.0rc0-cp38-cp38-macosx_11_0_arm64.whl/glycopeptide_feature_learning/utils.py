import random
import logging
from scipy.spatial.distance import pdist, squareform
import numpy as np


logger = logging.getLogger("glycopeptide_feature_learning")
logger.addHandler(logging.NullHandler())

def distcorr(X, Y, pval=False, nruns=500):
    """https://gist.github.com/satra/aa3d19a12b74e9ab7941
    """
    X_ = X
    Y_ = Y
    X = np.atleast_1d(X)
    Y = np.atleast_1d(Y)
    if np.prod(X.shape) == len(X):
        X = X[:, None]
    if np.prod(Y.shape) == len(Y):
        Y = Y[:, None]
    X = np.atleast_2d(X)
    Y = np.atleast_2d(Y)
    n = X.shape[0]
    if Y.shape[0] != X.shape[0]:
        raise ValueError('Number of samples must match')
    a = squareform(pdist(X))
    b = squareform(pdist(Y))
    A = a - a.mean(axis=0)[None, :] - a.mean(axis=1)[:, None] + a.mean()
    B = b - b.mean(axis=0)[None, :] - b.mean(axis=1)[:, None] + b.mean()

    dcov2_xy = (A * B).sum() / float(n * n)
    dcov2_xx = (A * A).sum() / float(n * n)
    dcov2_yy = (B * B).sum() / float(n * n)
    dcor = np.sqrt(dcov2_xy) / np.sqrt(np.sqrt(dcov2_xx) * np.sqrt(dcov2_yy))
    if pval:
        greater = 0
        for i in range(nruns):
            Y_r = Y_.copy()
            random.shuffle(Y_r)
            if distcorr(X_, Y_r, pval=False) > dcor:
                greater += 1
        return (dcor, greater / float(nruns))
    return dcor


def cosine_similarity(X, Y):
    return X.dot(Y) / (np.sqrt(X.dot(X)) * np.sqrt(Y.dot(Y)))
