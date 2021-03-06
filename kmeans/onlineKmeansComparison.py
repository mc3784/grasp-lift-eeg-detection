import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
from memory_profiler import memory_usage
import timeit
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.cluster import MiniBatchKMeans

def getPermutation(totalRange,numberElements):
    random_seed = 10312003
    rng = np.random.RandomState(random_seed)
    permutation = rng.permutation(totalRange)
    return permutation[:numberElements]

def onlineKmeans(X,k=3,b=30,maxiter=1000):
    centroids = X[getPermutation(len(X),k)]
    pointsPerClusters = np.zeros([k,1])
    minInertia=0
    notImproveCount=0
    for i in range(maxiter):
        M=X[getPermutation(len(X),b)]
        distances = pairwise_distances(M, centroids, metric='euclidean')
        nearestCenters = np.argmin(distances, axis=1)
        inertia = np.sum(np.amin(distances, axis=1))  
        if (minInertia ==0 or inertia < minInertia):
            minInertia = inertia
            notImproveCount=0
        elif minInertia !=0 and inertia >= minInertia:
            notImproveCount+=1
        if (notImproveCount>10): 
            break
        for iter, x in enumerate(M):
            centerIndex = nearestCenters[iter]
            pointsPerClusters[centerIndex] = pointsPerClusters[centerIndex] + 1
            eta = 1/pointsPerClusters[centerIndex]
            centroids[centerIndex] = (1 - eta)*centroids[centerIndex] + eta * x
    return centroids

def profile_memory_and_time(function, *args, **kwargs):
    start_time = timeit.default_timer()
    memory, return_val = memory_usage((function, (args), kwargs), max_usage=True, retval=True)
    elapsed = timeit.default_timer() - start_time
    return memory[0], elapsed,return_val


iris = load_iris()
X=iris.data
random_seed = 10312003
rng = np.random.RandomState(random_seed)
permutation = rng.permutation(len(X))
X = X[permutation]
ourMemory,ourTime,ourCentroids= profile_memory_and_time(onlineKmeans, X, k=3, b=33, maxiter=1000)

minibatch=MiniBatchKMeans(n_clusters=3,max_iter=100,batch_size=33)
memory, time, rval = profile_memory_and_time(minibatch.fit,X)

inputSizesToGenerate = [[2**8, 32],[2**10, 32],[2**12, 32],[2**14, 32],
                        [2**16, 32],[2**18, 32],[2**20, 32],[2**22, 32]]
                        #[2**24, 32],[2**26, 32],[2**28, 32],[2**30, 32],[2**32, 32]];

scaler = StandardScaler()
plt.ion()
f1 = plt.figure()
ax1 = f1.add_subplot(111)
ourTimes=[]
times=[]
ourMemories=[]
memoris=[]
numSamples=[]

for num_samples, num_dimension in inputSizesToGenerate:
    print "Running for {0} samples of dimension {1}".format(num_samples, num_dimension)
    X,y = make_blobs(n_samples=num_samples, n_features=num_dimension, centers=6)
    scaler.fit(X)
    X_scaled = scaler.transform(X)
    
    ourMemory,ourTime,ourCentroids= profile_memory_and_time(onlineKmeans, X, k=3, b=33, maxiter=1000)
    ourTimes.append(ourTime)
    ourMemories.append(ourMemory)
    memory, time, rval = profile_memory_and_time(minibatch.fit,X)
    times.append(time)
    memoris.append(memory)
    
    numSamples.append(num_samples)
plt.scatter(numSamples, ourMemories,color="green",label="online Keameans")
plt.scatter(numSamples, memoris,color="red",label="sklearn Kmeans")
plt.title("MEMORY")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
plt.savefig('memory.png')
plt.clf()
plt.scatter(numSamples, ourTimes,color="green",label="online Keameans")
plt.scatter(numSamples, times,color="red",label="sklearn Kmeans")
plt.title("TIME")
plt.show()
plt.savefig('time.png')
    
