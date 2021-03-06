from sklearn.datasets import load_iris
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import pairwise_distances

import cProfile


def getPermutation(totalRange,numberElements):
    random_seed = 10312003
    rng = np.random.RandomState(random_seed)
    permutation = rng.permutation(totalRange)
    return permutation[:numberElements]


def onlineKmeans(X,k=3,b=30,maxiter=1000):
    centroids = X[getPermutation(len(X),k)]
    pointsPerClusters = np.zeros([k,1])
    for i in range(maxiter):
        M=X[getPermutation(len(X),b)]
        distances = pairwise_distances(M, centroids, metric='euclidean')
        nearestCenters = np.argmin(distances, axis=1)
        for iter, x in enumerate(M):
            centerIndex = nearestCenters[iter]
            pointsPerClusters[centerIndex] = pointsPerClusters[centerIndex] + 1
            eta = 1/pointsPerClusters[centerIndex]
            centroids[centerIndex] = (1 - eta)*centroids[centerIndex] + eta * x

    return centroids


iris = load_iris()
X=iris.data
random_seed = 10312003
rng = np.random.RandomState(random_seed)
permutation = rng.permutation(len(X))
X = X[permutation]
onlineKmeans(X)    

