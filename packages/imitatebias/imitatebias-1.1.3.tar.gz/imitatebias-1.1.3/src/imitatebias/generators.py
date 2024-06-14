import numpy as np


# Generation of Cov:
# Cholesky decomposition: for every real-valued symmetric positive-definite (SPD) matrix M, there is a 
#   unique lower-diagonal matrix L with positive diagonal entries and LL^T = M
# => I generate lower-diagonal matrices m with positive diagonal and get Cov=mm^T !
def generateData(num_instances, num_clusters, num_dims, return_params=False, seed=None, mean_low=1, mean_high=100):
    """Generates random data drawn from multivariate Gaussian(s).
    
    The covariance matrices of the multivariate Gaussians are generated randomly
    via their Cholesky decomposition (i.e., for every real-valued symmetric positive-
    definite (SPD) matrix M, there is a unique lower-diagonal matrix L with positive
    diagonal entries and LL^T = M). That is, we generate lower-diagonal matrices m
    with positive diagonal and obtain the covariance matrices as Cov = mm^T.
    
    Parameters
    ----------
    num_instances : int (> 0)
        The size of the generated dataset.
    num_clusters : int (> 0)
        The number of clusters / classes in the generated dataset.
    num_dims : int (> 0)
        The dimensionality of the generated dataset.
    return_params : bool, default=False
        Returns (data, labels, parameters) of the generated Gaussians alongside the
        data and labels that are returned either way.
    seed : int, optional
        The random seed for reproducible generation of the dataset.
    mean_low : float, default=1
        Controls the range in which the means of the Gaussians are generated (lower
        boundary).
    mean_high : float, default=100
        Controls the range in which the means of the Gaussians are generated (upper
        boundary).
    
    Returns
    -------
    np.ndarray (2D)
        Generated data points.
    np.array (1D)
        Corresponding class / cluster labels. 
    
    Examples
    --------
    >>> from imitatebias.generators import *
    >>> import matplotlib.pyplot as plt

    Generate a dataset.
    >>> X, y = generateData(1000, 2, 2, seed=2210)

    Plot the dataset.
    >>> plt.scatter(X[:,0], X[:,1], c=y)
    >>> plt.show()
    """
    rng = np.random.default_rng(seed)
    points = np.empty((0,num_dims))
    labels = []
    params = []
    num_cl = ([num_instances // num_clusters + (1 if x < num_instances % num_clusters else 0)  for x in range (num_clusters)])
    for i in range(len(num_cl)):
        
        # generate Cov using Cholesky decomposition
        m = rng.integers(1,50)*(2*rng.random((num_dims, num_dims))-1)
        for j in range(len(m)):
            m[j,j] = np.abs(m[j,j])
        m = np.tril(m)
        cov = m.dot(m.transpose())
        
        # generate mean
        mean = rng.integers(mean_low,mean_high)*(2*rng.random(num_dims)-1)
        
        # sample points
        pts = rng.multivariate_normal(mean, cov, size=num_cl[i])
        
        points = np.concatenate((points, pts), axis=0)
        labels = np.append(labels, [i]*num_cl[i])
        params.append([mean, cov])
    if return_params: return points, np.array(labels), params
    return points, np.array(labels)


def generateBias(data, labels, num_biasedClusters, prob=0.05, seed=None):
    """Generates an artificial bias.
    
    A dataset sampled from a multivariate Gaussian is biased by rotating a hyper-
    plane around its center by a random angle. Most data points (the user controls how
    many) above the hyperplane are removed. This bias generation strategy has been 
    described in our paper [1].
    
    Parameters
    ----------
    data : np.ndarray (2D)
        The dataset to be biased artificially. 
    labels : np.array (1D)
        The corresponding set of labels indicating classes / clusters.
    num_biasedClusters : int (> 0)
        The number of clusters in the dataset that should be biased.
    prob : float, default=0.05
        The probability for each point above the random hyperplane to remain in the 
        dataset.
    seed : int, optional
        The random seed for reproducible generation of the bias.
    
    Returns
    -------
    np.ndarray (2D)
        The biased dataset.
    np.array (1D)
        The corresponding labels.
    np.array (1D)
        The list of indices of points in the original dataset that have been removed.

    References
    ----------
    .. [1] Katharina Dost, Katerina Taskova, Patricia Riddle, and Jörg Wicker. 
       "Your Best Guess When You Know Nothing: Identification and Mitigation of 
       Selection Bias." In: 2020 IEEE International Conference on Data Mining (ICDM), 
       pp. 996-1001, IEEE, 2020, ISSN: 2374-8486.
        
    Examples
    --------
    >>> from imitatebias.generators import *
    >>> import matplotlib.pyplot as plt

    Generate a dataset.
    >>> X, y = generateData(1000, 2, 2, seed=2210)

    Generate a biased dataset.
    >>> X_b, y_b, idcs_deleted = generateBias(X, y, 1, seed=2210)

    Plot the biased dataset.
    >>> plt.scatter(X_b[:,0], X_b[:,1], c=y_b)
    Plot the removed points.
    >>> plt.scatter(X[idcs_deleted,0], X[idcs_deleted,1], c='red', label='deleted points')
    >>> plt.legend()
    >>> plt.show()
    """
    rng = np.random.default_rng(seed)
    delete_this = []
    clusters = np.unique(labels)
    if num_biasedClusters > len(clusters): num_biasedClusters = len(clusters)
    
    # select blobs that will be biased
    bias_these = rng.choice(clusters, num_biasedClusters, replace=False)
    alphas = rng.random(num_biasedClusters) * 2*np.pi # angle for plane
    for blob, alpha in zip(bias_these, alphas):
        dims = rng.choice(range(len(data[0])), 2, replace=False)
        mean = data[labels == blob].mean(0)[dims]
        d = np.sqrt(np.sum((data[:,dims] - mean)**2, axis=1))
        angles = np.arcsin((data[:, dims[1]] - mean[1]) / d)
        angles = np.array([(np.pi - angles[i] if data[i, dims[0]] < mean[0] else angles[i]) for i in range(len(angles))])
        angles[angles < 0] += 2*np.pi
        if alpha >= np.pi:
            b = np.logical_or(angles > alpha, angles < alpha - np.pi)
        else:
            b = np.logical_and(angles > alpha, angles < (alpha + np.pi) % (2 * np.pi))
        b = np.logical_and(b, labels == blob)
        b = np.where(b)[0]
        b = np.delete(b, rng.choice(range(len(b)), int(prob*len(b)), replace=False))
        delete_this = np.append(delete_this, b)
        
    delete_this = delete_this.astype(int)
    d, l = np.delete(data, delete_this, axis=0), np.delete(labels, delete_this)
    return d, l, delete_this